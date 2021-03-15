from abc import ABC

from rest_messaging.models import Message

from celery import shared_task


@shared_task
def sent_message(message_id: int) -> None:
    """
    Send message imitation

    Args:
        message_id: message id
    """
    message = Message.objects.get(id=message_id)
    message.is_sent = True
    message.save()
