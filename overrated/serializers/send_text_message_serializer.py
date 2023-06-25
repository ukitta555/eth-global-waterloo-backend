from django.db.migrations import serializer
from rest_framework import serializers

from overrated.models import MyUser, TextMessage


class SendTextMessageSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField(
        label="ReceiverEmail"
    )
    message_text = serializers.CharField(
        label="TextMessage"
    )

    # I know that I'm using serializers wrong, we're behind the schedule a bit
    def validate(self, attrs):
        receiver_email = attrs.get("receiver_email")
        message_text = attrs.get("message_text")
        if receiver_email and message_text:
            recipient_qs = MyUser.objects.filter(email=receiver_email)
            if not recipient_qs.exists():
                msg = 'No such user exists!'
                raise serializers.ValidationError(msg, code=400)
            recipient = recipient_qs[0]
            TextMessage.objects.create(
                message_text=message_text,
                user=recipient
            )
        return message_text
