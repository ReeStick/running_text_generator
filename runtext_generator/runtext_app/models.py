from django.db import models

class RequestLog(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    get_arguments = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)  # Добавляем поле body

    @classmethod
    def create_log(cls, method, path, get_arguments, body=None):
        log_entry = cls(method=method, path=path, get_arguments=get_arguments, body=body)
        log_entry.save()