from django.contrib.auth.models import AbstractUser
from django.db import models


class Client(AbstractUser):
    """Переопределение абстрактной модели пользователя"""

    username = None
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars", verbose_name="Аватар")
    numbers_phone = models.CharField(null=True, blank=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=300, null=True, blank=True, verbose_name="Город")
    full_username = models.TextField(null=True, blank=True, verbose_name=" Ф.И.О.")
    comment = models.TextField(null=True, blank=True)

    token = models.TextField(
        null=True,
        blank=True,
        unique=True,
    )
    email = models.EmailField(unique=True, verbose_name="почта", null=False, blank=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"<{self.username} {self.email}>"


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="почта", null=False, blank=False)
    full_username = models.TextField(null=True, blank=True, verbose_name=" Ф.И.О.")



    def __str__(self):
        return f"<{self.email}>"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"