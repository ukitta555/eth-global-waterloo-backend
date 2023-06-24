import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from overrated.models import MyUser


class RegisterSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(
        label="Email",
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    additional_reputation = serializers.IntegerField(
        label="Additional Reputation",
        trim_whitespace=True,
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')
        additional_reputation = attrs.get('additional_reputation')
        if email and password and additional_reputation > 0:
            user = MyUser.objects.create(
                email=email,
                password=make_password(password),
                public_key="",
                date_of_birth=datetime.date(year=2000, month=1, day=1),
                additional_reputation_for_phantom_account=additional_reputation,
                last_reputation_bump_for_phantom_account=datetime.datetime.now()
            )
        else:
            msg = '"username","password" and positive reputation bump are required.'
            raise serializers.ValidationError(msg, code=400)
        return user