from celery import Celery
from flask import Flask
from datetime import timedelta
from app import create_app

def make_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

flask_app = create_app()
flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TIMEZONE='UTC',
    CELERYBEAT_SCHEDULE={
        'daily-service-reminders': {
            'task': 'app.tasks.send_daily_reminders',
            'schedule': timedelta(days=1),
            'options': {'expires': 3600}
        },
        'monthly-activity-reports': {
            'task': 'app.tasks.send_monthly_reports',
            'schedule': timedelta(days=30),
            'options': {'expires': 7200}
        }
    }
)

celery = make_celery(flask_app)

# Celery configuration
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_ENABLE_UTC = True 