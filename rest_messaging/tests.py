import csv
import io
from django.test import TestCase

from rest_messaging.models import Message


class MessageTestCase(TestCase):
    """
    Test message creation
    """
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


class MessageCSVTestCase(TestCase):
    """
    Test message sending
    """
    def test_csv_export(self):
        response = self.client.get('/rest_messaging/posts/download')
        self.assertEqual(response.status_code, 200)

        content = response.content.decode('utf-8')
        cvs_reader = csv.reader(io.StringIO(content))
        body = list(cvs_reader)
        messages = Message.objects.all()
        headers = body.pop(0)
        message_fields = Message._meta.fields
        self.assertEquals(
            messages.count(),
            len(body)
        )
        self.assertEquals(
            len(message_fields),
            len(headers)
        )
