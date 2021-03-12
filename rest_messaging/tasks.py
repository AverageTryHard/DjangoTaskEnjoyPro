import string

from rest_messaging.models import Message

from celery import shared_task


@shared_task
def sent_message(message_id):
    message = Message.objects.get(pk=message_id)
    message.is_sent = True
    message.save()
    return "Message with title '{}' was sent!".format(message.title)
