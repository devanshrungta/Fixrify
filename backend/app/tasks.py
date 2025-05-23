from app import db
from app.models.user import User
from app.models.service import ServiceRequest
from datetime import datetime, timedelta
import csv
from io import StringIO
import requests
from flask import current_app, render_template
from flask_mail import Mail, Message
from app.extensions import cache
from app.utils.email import send_email
from sqlalchemy import and_
import os
from celery import Celery

mail = Mail()

import app
from celery import Task
class taskContext(Task):
    def __call__(self, *args, **kwargs):
        with app.create_app().app_context():
            return self.run(*args, **kwargs)

celery = Celery(
    broker_url="redis://localhost:6379/1",
    result_backend="redis://localhost:6379/2"
)

from celery.schedules import crontab
celery.conf.beat_schedule = {
    # 'trigger-add-helloWorld-every-10-seconds':{
    #     'task': 'app.tasks.helloWorld',
    #     'schedule': 10.0,
    # },
    # 'test-mail':{
    #     'task': 'app.tasks.test_email',
    #     'schedule': crontab(hour=14, minute=23)
    # },
    'trigger-daily-reminder':{
        'task': 'app.tasks.send_daily_reminders',
        'schedule': crontab(hour=23, minute=30)
    },
    'trigger-monthly-mail':{
        'task': 'app.tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=29, hour=21, minute=37)
    }
}

@celery.task(base = taskContext)
def helloWorld():
    print('this is the first test task')
    return 'hello world'

@celery.task(base = taskContext)
def test_email():
    """Test email functionality"""
    send_email(
        subject="Test Email from Fixrify",
        recipients=["test@example.com"],
        html_body="<h1>Test Email</h1><p>This is a test email from Fixrify.</p>"
    )
    return "Email sent successfully"

@celery.task(base = taskContext)
def send_daily_reminders():
    """Send daily reminders to professionals with pending service requests"""
    try:
        # Get all professionals with pending requests
        professionals = User.query.filter_by(role='professional').all()

        for professional in professionals:
            # Get pending requests for this professional
            pending_requests = ServiceRequest.query.filter(
                and_(
                    ServiceRequest.professional_id == professional.id,
                    ServiceRequest.status == 'pending'
                )
            ).all()

            if pending_requests:
                # Prepare email content
                email_content = render_template(
                    'email/daily_reminder.html',
                    professional=professional,
                    pending_requests=pending_requests,
                    now=datetime.utcnow()
                )

                # Send reminder email
                send_email(
                    subject="You have pending service requests",
                    recipients=[professional.email],
                    html_body=email_content
                )
                current_app.logger.info(f"Daily reminder sent to {professional.email}")

        return "Daily reminders sent successfully"
    except Exception as e:
        current_app.logger.error(f"Error sending daily reminders: {str(e)}")
        raise

@celery.task(base = taskContext)
def send_monthly_reports():
    """Generate and send monthly activity report to customers"""
    try:
        # Get all customers
        customers = User.query.filter_by(role='customer').all()

        # Get last month's date range
        today = datetime.utcnow()
        first_of_this_month = datetime(today.year, today.month, 1)
        last_month_end = first_of_this_month - timedelta(days=1)
        last_month_start = datetime(last_month_end.year, last_month_end.month, 1)

        for customer in customers:
            # Get customer's service requests for last month
            requests = ServiceRequest.query.filter(
                and_(
                    ServiceRequest.customer_id == customer.id,
                    ServiceRequest.created_at >= last_month_start,
                    ServiceRequest.created_at < first_of_this_month
                )
            ).all()

            # Calculate statistics
            stats = {
                'total_requests': len(requests),
                'completed_requests': sum(1 for r in requests if r.status == 'completed'),
                'pending_requests': sum(1 for r in requests if r.status == 'pending'),
                'cancelled_requests': sum(1 for r in requests if r.status == 'cancelled'),
                'total_spent': sum(r.service.base_price for r in requests if r.status == 'completed')
            }

            # Generate report
            report_html = render_template(
                'email/monthly_report.html',
                customer=customer,
                stats=stats,
                requests=requests,
                month=last_month_start.strftime('%B %Y'),
                now=datetime.utcnow()
            )

            # Send report email
            send_email(
                subject=f"Your Monthly Activity Report - {last_month_start.strftime('%B %Y')}",
                recipients=[customer.email],
                html_body=report_html
            )
            current_app.logger.info(f"Monthly report sent to {customer.email}")

        return "Monthly reports sent successfully"
    
    except Exception as e:
        current_app.logger.error(f"Error sending monthly reports: {str(e)}")
        raise

@celery.task(base=taskContext)
def generate_service_requests_csv():
    """Generate a CSV file for all service requests."""
    try:
        # Get all service requests from the database
        service_requests = ServiceRequest.query.all()

        # Prepare CSV content
        output = StringIO()
        writer = csv.writer(output)

        # Write header
        writer.writerow([
            'ID', 'Customer', 'Service', 'Professional', 'Status', 'Address', 'Preferred Date', 'Created At', 'Completion Date', 'Actual Price'
        ])

        # Write service requests data
        for request in service_requests:
            writer.writerow([
                request.id,
                request.customer.name,
                request.service.name,
                request.professional.name if request.professional else 'Not Assigned',
                request.status,
                request.address,
                request.preferred_date,
                request.created_at.strftime('%Y-%m-%d'),
                request.completed_at.strftime('%Y-%m-%d') if request.completed_at else '',
                request.final_price
            ])

        # Store the CSV content in cache (using task ID as cache key)
        cache_key = f"service_requests_csv_{generate_service_requests_csv.request.id}"
        cache.set(cache_key, output.getvalue(), timeout=3600)  # Cache for 1 hour

        # Return the cache key to the client
        return cache_key

    except Exception as e:
        current_app.logger.error(f"Error generating CSV: {str(e)}")
        raise
