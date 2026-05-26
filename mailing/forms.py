from django import forms

from client.models import Recipient


class RecipientForm(forms.ModelForm):
    """Форма для создания/редактирования получателя"""

    class Meta:
        model = Recipient
        fields = ["email", "full_username"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "example@mail.com", "autofocus": True}
            ),
            "full_username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов Иван Иванович"}),
        }
        labels = {"email": "Email адрес", "full_username": "Ф.И.О."}

    def clean_email(self):
        """Валидация email на уникальность"""
        email = self.cleaned_data.get("email")

        # При редактировании исключаем текущий объект
        if self.instance and self.instance.pk:
            if Recipient.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Получатель с таким email уже существует!")
        else:
            if Recipient.objects.filter(email=email).exists():
                raise forms.ValidationError("Получатель с таким email уже существует!")

        return email

    def clean_full_username(self):
        """Очистка ФИО от лишних пробелов"""
        full_username = self.cleaned_data.get("full_username")
        if full_username:
            # Удаляем лишние пробелы и делаем заглавными первые буквы
            full_username = " ".join(full_username.split()).title()
        return full_username
