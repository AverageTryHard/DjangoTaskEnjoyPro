from django.test import TestCase

from rest_messaging.models import Message
from django.test import Client


class MessageTestCase(TestCase):
    def test_message(self):
        self.assertEquals(
            Message.objects.count(),
            0
        )
        Message.objects.create(
            title='TestMessage1', text_body='TestText1'
        )
        Message.objects.create(
            title='TestMessage2', text_body='TestText2'
        )
        self.assertEquals(
            Message.objects.count(),
            2
        )

# TODO client methods: message_read, message_csv
