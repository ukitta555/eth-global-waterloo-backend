from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework import views
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from overrated.serializers.login_serializer import LoginSerializer


class LogoutView(views.APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"msg": "OK logged out"}, status=status.HTTP_200_OK)