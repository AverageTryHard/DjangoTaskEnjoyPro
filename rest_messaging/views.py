import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import Throttled
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from ratelimit.decorators import ratelimit
from ratelimit.exceptions import Ratelimited
from backoff import on_exception, expo

from rest_messaging.models import Message
from rest_messaging.serializers import MessageSerializer
from csv_export.views import ModelCSVExportView
from DjangoTaskEnjoyPro.tasks import sent_message

logger = logging.getLogger('error_logger')


class MessageListAPIView(ListAPIView):
    """
    API view to retrieve list of messages
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


class MessageDetailsAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete message
    """
    serializer_class = MessageSerializer
    queryset = Message.objects


def create_limit_method(details: dict):
    """
    After limit of creating messages reached write in log and raise error 429

    Args:
        details: Full method info

    Raises:
        Throttled - Too many request, error with status 429
    """
    method_name = 'posts/create/ - create message method'
    client_ip = details['args'][0].META['REMOTE_ADDR']
    logger.error(f'ERROR: 429 error in method - {method_name}, request was sent by client with ip - {client_ip}')
    raise Throttled


@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@on_exception(expo, Ratelimited, on_backoff=create_limit_method)  # catch limit exception
@ratelimit(key='ip', rate='5/m', method='POST', block=True)  # limit amount of requests
def create_message(request):
    """
    Create new message

    Args:
        request: request

    Returns:
        Response with message data
    """
    body = json.loads(request.body)
    message = Message.objects.create(title=body['title'])
    sent_message.delay(message.pk)
    return Response(model_to_dict(message), status=status.HTTP_201_CREATED)


@csrf_exempt
def read_message(request, message_id: int) -> HttpResponse:
    """
    Set is_read of message True

    Args:
        request: request
        message_id: message table id

    Returns:
        HttpResponse: response with status code
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    message = get_object_or_404(Message.objects, pk=message_id)
    message.is_read = True
    message.save()
    return HttpResponse(staticmethod=200)


class MessageCsvExport(ModelCSVExportView):
    """
    Export csv file with message data
    """
    def __init__(self, *args, **kwargs):
        super().__init__(MessageSerializer, Message, 'created_at', **kwargs)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
