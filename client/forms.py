from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from client.models import Client, Recipient


class CustomClientCreationForm(UserCreationForm):
    """Костамизация формы"""

    class Meta:
        model = Client
        fields = ["email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CustomClientCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {"class": "form-control border-start-0", "placeholder": "Введите email"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control border-start-0", "placeholder": "Введите пароль", "type": "password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control border-start-0", "placeholder": "Повторите пароль", "type": "password"}
        )


class BootstrapLoginForm(AuthenticationForm):
    """Костамизация формы"""

    def __init__(self, *args, **kwargs):
        super(BootstrapLoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control border-start-0", "placeholder": "Введите email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control border-start-0", "placeholder": "Введите пароль", "type": "password"}
        )
