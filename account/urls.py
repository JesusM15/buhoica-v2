from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('iniciar-sesion/', auth_views.LoginView.as_view(), name='login'),
    path('sesion-cerrada/', auth_views.LogoutView.as_view(), name='logout'),
    
    #cambiar contraseñas
    
    #resetear contraseña
    
    #registrarse
    path('registrarse/', views.register, name='register'),
    
    #cuenta
    path('perfil/<int:user_id>/<username>/', views.profile, name='profile'),
    
    
]