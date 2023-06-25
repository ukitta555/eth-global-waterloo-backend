
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from overrated.models import TextMessage
from overrated.serializers.text_message_serializer import TextMessageSerializer


class TextMessageViewSet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self, **kwargs):
        user = kwargs.get("user")
        queryset = TextMessage.objects.all()
        queryset = queryset.filter(user=user)
        return queryset

    def get(self, request):
        user = self.request.user
        result = self.get_queryset(user=user)
        serializer = TextMessageSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)