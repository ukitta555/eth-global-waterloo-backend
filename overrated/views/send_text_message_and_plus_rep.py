from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from overrated.serializers.send_text_message_and_plus_rep_serializer import SendTextMessageAndPlusRepSerializer


class SendTextMessageAndPlusRep(APIView):
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
        return Response("OK", status=status.HTTP_201_CREATED)