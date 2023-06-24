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
    public_key = serializers.CharField(
        label="Public key",
        trim_whitespace=True,
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')
        public_key = attrs.get('public_key')
        # TODO: add check whether it is a valid hex num
        if len(public_key) != 42:
            msg = '"public_key" should have length 42.'
            raise serializers.ValidationError(msg, code=400)
        if email and password and public_key:
            # Try to authenticate the user using Django auth framework.
            user = MyUser.objects.create(
                email=email,
                password=make_password(password),
                public_key=public_key,
                date_of_birth=datetime.date(year=2000, month=1, day=1)

            )
        else:
            msg = '"username","password" and "public_key" are required.'
            raise serializers.ValidationError(msg, code=400)
        return user