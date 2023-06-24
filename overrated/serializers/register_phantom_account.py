import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from overrated.models import MyUser


class RegisterPhantomSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    sender_email = serializers.EmailField(
        label="Email",
    )
    recipient_email = serializers.EmailField(
        label="Email",
    )
    additional_reputation = serializers.IntegerField(
        label="Additional Reputation",
    )

    def validate(self, attrs):
        # Take username and password from request
        sender_email = attrs.get('sender_email')
        recipient_email = attrs.get('recipient_email')
        additional_reputation = attrs.get('additional_reputation')
        if sender_email and recipient_email and additional_reputation > 0:
            # TODO: check whether the sender has enough tokens
            user = MyUser.objects.create(
                email=recipient_email,
                password="",
                public_key="",
                date_of_birth=datetime.date(year=2000, month=1, day=1),
                additional_reputation_for_phantom_account=additional_reputation,
                last_reputation_bump_for_phantom_account=datetime.datetime.now()
            )
            # TODO: send email to the guy that is not yet on the platform
        else:
            msg = '"username","password" and positive reputation bump are required.'
            raise serializers.ValidationError(msg, code=400)
        return recipient_email
