from rest_framework import serializers

from rest_messaging.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('pk', 'title', 'text_body', 'is_sent', 'is_read', 'created_at', 'changed_at')
