from django.db import models

from client.models import Client, Recipient
from send_messages.models import Message


class Mailing(models.Model):
    NEW = "NEW"
    LAUNCHED = "LAU"
    COMPLETED = "COM"
    STATUS = [
        (NEW, "Создана"),
        (LAUNCHED, "Запущена"),
        (COMPLETED, "Завершена"),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS,
        default=NEW,
    )
    start_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата начала расслыки")
    end_time = models.DateTimeField(blank=True, null=True, verbose_name="Дата окончания рассылки")
    message = models.ForeignKey(Message, blank=True, null=True, verbose_name="Сообщение", on_delete=models.CASCADE)
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Владелец рассылки")
