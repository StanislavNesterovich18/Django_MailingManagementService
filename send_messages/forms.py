from django import forms
from django.core.exceptions import ValidationError

from .models import Message


class MessageForm(forms.ModelForm):
    """Форма для создания/редактирования сообщения"""

    class Meta:
        model = Message
        fields = ["subject_letter", "body_letter"]
        widgets = {
            "subject_letter": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите тему письма", "autofocus": True}
            ),
            "body_letter": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Введите текст сообщения...", "rows": 8}
            ),
        }
        labels = {"subject_letter": "Тема письма", "body_letter": "Текст сообщения"}

    def clean_subject_letter(self):
        """Валидация темы письма"""
        subject = self.cleaned_data.get("subject_letter")
        if subject and len(subject) > 200:
            raise ValidationError("Тема письма не должна превышать 200 символов")
        return subject

    def clean_body_letter(self):
        """Валидация текста письма"""
        body = self.cleaned_data.get("body_letter")
        if body and len(body) > 500:
            raise ValidationError("Текст письма не должен превышать 500 символов")
        return body

    def save(self, commit=True, owner=None):
        """Сохраняем сообщение с указанием владельца"""
        instance = super().save(commit=False)
        if owner:
            instance.owner = owner
        if commit:
            instance.save()
        return instance
