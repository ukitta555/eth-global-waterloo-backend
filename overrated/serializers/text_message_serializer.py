from rest_framework import serializers

from overrated.models import TextMessage


class TextMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextMessage
        fields = ['message_text']
