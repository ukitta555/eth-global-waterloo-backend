from django.contrib.auth import login
from rest_framework import permissions, status
from rest_framework import views
from rest_framework.response import Response

from overrated.serializers.login_serializer import LoginSerializer


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(
            data=self.request.data,
            context={
                'request': self.request
            })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({"email": user.email, "pub_key": user.public_key}, status=status.HTTP_202_ACCEPTED)