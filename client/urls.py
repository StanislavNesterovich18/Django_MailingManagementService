from django.contrib.auth.views import LoginView
from django.urls import path

from client import views
from client.apps import ClientConfig
from client.forms import BootstrapLoginForm

app_name = ClientConfig.name

urlpatterns = ([
    path("", LoginView.as_view(template_name="login.html",authentication_form=BootstrapLoginForm), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    path("email_validation/<str:token>/", views.token_valid, name="email_validation"),
])
