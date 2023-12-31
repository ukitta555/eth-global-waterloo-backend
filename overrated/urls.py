"""
URL configuration for eth_waterloo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from overrated.views.email_test import EmailTestView
from overrated.views.get_text_messages_viewset import TextMessageViewSet
from overrated.views.login import LoginView
from overrated.views.logout import LogoutView
from overrated.views.register import RegisterView
from overrated.views.register_phantom_account import RegisterPhantomView
from overrated.views.send_text_message import SendTextMessage
from overrated.views.test_auth_view import TestAuthView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('register-phantom/', RegisterPhantomView.as_view(), name="phantom_register"),
    path('email-test/', EmailTestView.as_view(), name="email_test"),
    path('test/', TestAuthView.as_view(), name="test"),
    path('send-message/', SendTextMessage.as_view(), name="send_message_to_person"),
    path('view-messages/', TextMessageViewSet.as_view(), name="get_messages"),
]
