from django.db import models


class Message(models.Model):
    subject_letter = models.CharField(max_length=200, blank=True, null=True, verbose_name="Тема письма")
    body_letter = models.CharField(max_length=500, blank=True, null=True, verbose_name="Тело письма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        "client.Client", on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject_letter if self.subject_letter else f"Сообщение #{self.id}"

    def get_short_body(self):
        """Возвращает короткую версию тела письма (первые 100 символов)"""
        if self.body_letter:
            return self.body_letter[:100] + "..." if len(self.body_letter) > 100 else self.body_letter
        return ""
