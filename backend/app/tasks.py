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

from celery import Task
from flask import current_app

class taskContext(Task):
    def __call__(self, *args, **kwargs):
        with current_app.app_context():
            return self.run(*args, **kwargs) 

celery = Celery(
    broker_url="redis://localhost:6379/1",
    result_backend="redis://localhost:6379/2",
)

@celery.task
def test_email(base = taskContext):
    """Test email functionality"""
    send_email(
        subject="Test Email from Fixrify",
        recipients=["test@example.com"],
        html_body="<h1>Test Email</h1><p>This is a test email from Fixrify.</p>"
    )
    return "Email sent successfully"

@celery.task
def send_daily_reminders(base = taskContext):
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

@celery.task
def send_monthly_reports(base = taskContext):
    """Generate and send monthly activity report to customers"""
    try:
        # Get all customers
        customers = User.query.filter_by(role='customer').all()
        
        for customer in customers:
            # Get last month's date range
            today = datetime.utcnow()
            first_of_month = datetime(today.year, today.month, 1)
            last_month_start = first_of_month - timedelta(days=first_of_month.day)
            
            # Get customer's service requests for last month
            requests = ServiceRequest.query.filter(
                and_(
                    ServiceRequest.customer_id == customer.id,
                    ServiceRequest.created_at >= last_month_start,
                    ServiceRequest.created_at < first_of_month
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

@celery.task
def export_service_requests_csv(base = taskContext):
    """Export completed service requests to CSV"""
    # Get all completed service requests
    service_requests = ServiceRequest.query.filter_by(status='completed').all()
    
    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Service ID', 'Customer ID', 'Professional ID',
        'Date of Request', 'Date of Completion',
        'Status', 'Actual Price', 'Remarks'
    ])
    
    # Write data
    for request in service_requests:
        writer.writerow([
            request.service_id,
            request.customer_id,
            request.professional_id,
            request.created_at.strftime('%Y-%m-%d'),
            request.completion_date.strftime('%Y-%m-%d') if request.completion_date else '',
            request.status,
            request.actual_price,
            request.remarks
        ])
    
    # Save to file
    filename = f'service_requests_{datetime.utcnow().strftime("%Y%m%d")}.csv'
    with open(filename, 'w') as f:
        f.write(output.getvalue())
    
    return filename

@celery.task
def generate_service_requests_csv(base = taskContext):
    # Get all service requests
    requests = ServiceRequest.query.all()
    
    # Create a CSV file
    filename = f'service_requests_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    filepath = os.path.join('exports', filename)
    
    # Ensure exports directory exists
    os.makedirs('exports', exist_ok=True)
    
    # Write data to CSV
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Customer', 'Service', 'Professional', 'Status', 'Address', 'Preferred Date', 'Created At'])
        
        for request in requests:
            writer.writerow([
                request.id,
                request.customer.name,
                request.service.name,
                request.professional.name if request.professional else 'Not Assigned',
                request.status,
                request.address,
                request.preferred_date,
                request.created_at
            ])
    
    return filepath 