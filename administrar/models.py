from django.db import models
from account.models import *
from django.conf import settings

class Solicitud(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitud')
    creado = models.DateField(auto_now_add=True)
    class Meta:verbose_name_plural = 'Solicitudes'