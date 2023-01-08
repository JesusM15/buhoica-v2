from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    # direccion = models.TextField()
    ciudad = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=200, blank=True)
    calle = models.CharField(max_length=200, blank=True)
    administrador = models.BooleanField(default=False)
    
    def __str__(self):return f'Perfil de {self.user.username}'