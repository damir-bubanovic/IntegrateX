from celery import shared_task
from django.utils import timezone
from apps.integrations.models import WebhookEvent


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def process_webhook_event(self, webhook_event_id: str) -> str:
    event = WebhookEvent.objects.select_related("integration").get(id=webhook_event_id)

    event.status = WebhookEvent.Status.PROCESSING
    event.attempts += 1
    event.last_error = ""
    event.save(update_fields=["status", "attempts", "last_error"])

    try:
        if not event.signature_valid:
            # do not retry invalid signatures
            event.status = WebhookEvent.Status.FAILED
            event.last_error = "Invalid webhook signature"
            event.processed_at = timezone.now()
            event.save(update_fields=["status", "last_error", "processed_at"])
            return "invalid_signature"

        # TODO: provider-specific handling will go here in later steps

        event.status = WebhookEvent.Status.SUCCEEDED
        event.processed_at = timezone.now()
        event.save(update_fields=["status", "processed_at"])
        return "ok"

    except Exception as exc:
        event.status = WebhookEvent.Status.FAILED
        event.last_error = str(exc)
        event.save(update_fields=["status", "last_error"])
        raise self.retry(exc=exc)
