from django.db import models

from client.models import Client
from send_messages.models import Message


class MailingRecipient(models.Model):
    email = models.CharField(unique=True, max_length=200)
    attempt_time = models.DateTimeField(auto_now_add=True)
    full_username = models.TextField(null=True, blank=True, verbose_name=" Ф.И.О.")
    comment = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    server_response = models.TextField(null=True, blank=True)


class Mailing(models.Model):
    NEW = "NEW"
    LAUNCHED = "LAU"
    COMPLETED = "COM"
    STATUS = {
        NEW: 'Создана',
        LAUNCHED: 'Запущена',
        COMPLETED: 'Завершена',
    }
    status = models.CharField(
        max_length=3,
        choices=STATUS,
        default=LAUNCHED,
    )
    start_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата начала расслыки")
    end_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата окончания рассылки")
    message = models.ForeignKey(Message, blank=True, null=True, verbose_name="Сообщение", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient, verbose_name="Получатели")
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Владелец рассылки")
