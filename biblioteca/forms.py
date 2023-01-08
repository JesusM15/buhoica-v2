from django import forms 
from .models import *

class CommentFormFisico(forms.ModelForm):
    class Meta:
        model = Comentario_f
        fields = ['cuerpo']
        
class CommentFormDigital(forms.ModelForm):
    class Meta:
        model = Comentario_d
        fields = ['cuerpo']
        
class UploadBookForm(forms.ModelForm):
    class Meta:
        model = Fisico
        fields = ['titulo', 'autor', 'precio', 'link_de_compra', 'unidades', 'imagen', 'descripcion', 'fecha_de_publicacion', 'tags', ]        

class UploadEBookForm(forms.ModelForm):
    class Meta:
        model = Digital
        fields = ['titulo', 'autor', 'precio', 'pdf', 'imagen', 'descripcion', 'fecha_de_publicacion', 'tags', ]        

# class UploadFBookForm(forms.ModelForm):
#     class Meta:
#         model = Fisico
#         fields = [ ]

# class UploadDBookForm(forms.ModelForm):
#     class Meta:
#         model = Digital
#         fields = ['pdf']

