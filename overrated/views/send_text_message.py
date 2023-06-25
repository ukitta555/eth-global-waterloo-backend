from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from overrated.serializers.send_text_message_serializer import SendTextMessageSerializer


class SendTextMessage(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SendTextMessageSerializer(
            data=self.request.data,
            context={
                'request': self.request
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(f"Message f{serializer.validated_data} sent", status=status.HTTP_201_CREATED)
