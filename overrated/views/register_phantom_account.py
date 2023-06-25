import os

from dotenv import load_dotenv
from rest_framework import status
from rest_framework import views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from overrated.serializers.register_phantom_account import RegisterPhantomSerializer

dotenv_path = os.path.join('/home/vladyslav/PycharmProjects/eth_waterloo_backend/eth_waterloo_backend/.env')
load_dotenv(dotenv_path)

class RegisterPhantomView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = RegisterPhantomSerializer(
            data=self.request.data,
            context={
                'request': self.request
            })
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "email": serializer.validated_data,
            },
            status=status.HTTP_201_CREATED,
        )