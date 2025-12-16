from celery import shared_task
from apps.notifications.services.email_service import send_notification_email


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_email_task(self, to_email: str, subject: str, message: str) -> str:
    try:
        send_notification_email(to_email=to_email, subject=subject, message=message)
        return "sent"
    except Exception as exc:
        raise self.retry(exc=exc)
