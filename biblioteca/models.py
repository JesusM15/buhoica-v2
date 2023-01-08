from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from taggit.managers import TaggableManager

class Libro(models.Model):
    titulo = models.CharField(max_length=300)
    descripcion = models.TextField()
    autor = models.CharField(max_length=200)
    slug = models.SlugField(max_length=400, unique=True)
    imagen = models.ImageField(upload_to='imagen/libro/%Y/%m/%d')
    precio = models.DecimalField(max_digits=100000, decimal_places=2)
    tags = TaggableManager()
    show = models.BooleanField(default=True)
    fecha_de_publicacion = models.DateField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):return f'{self.titulo}'
    
    def save(self, *args, **kwargs):
        if not self.slug:self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)
    
    class Meta:abstract = True
        
class Digital(Libro):
    pdf = models.FileField(upload_to='pdf/%Y/%m/%d')
    users_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='digital_liked', blank=True)
    def get_absolute_url(self): return reverse('detail_d', args=[self.slug, self.creado])
    class Meta:verbose_name_plural = 'Digitales'
    
class Fisico(Libro):
    link_de_compra = models.URLField(max_length=2000)
    unidades = models.PositiveIntegerField(default=1)
    users_likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='fisico_liked', blank=True)
    def get_absolute_url(self): return reverse('detail_f', args=[self.slug, self.creado])

class Comentario_f(models.Model):
    book = models.ForeignKey(Fisico, on_delete=models.CASCADE, related_name='fcomments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userf_comments')
    cuerpo = models.TextField()
    revision = models.BooleanField(default=False)
    creado = models.DateField(auto_now_add=True)
    
    def __str__(self):return f'Comentario de {self.user} en {self.book}'

class Comentario_d(models.Model):
    book = models.ForeignKey(Digital, on_delete=models.CASCADE, related_name='dcomments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userd_comments')
    cuerpo = models.TextField()
    revision = models.BooleanField(default=False)
    creado = models.DateField(auto_now_add=True)
    
    def __str__(self):return f'Comentario de {self.user} en {self.book}'
