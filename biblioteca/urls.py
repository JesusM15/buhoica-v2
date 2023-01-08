from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),  
    path('ordenar/<ordenar>/', views.homePage, name='home_p'),  
    path('libros/f/<slug:book_slug>/<creado>/', views.detail_pageF, name='detail_f'),
    path('libros/d/<slug:book_slug>/<creado>/', views.detail_pageD, name='detail_d'),
    path('libros/comentario/<type>/<int:book_id>/<user>/', views.book_comment, name='book_comment'),
    path('like/', views.like, name='like'),
    path('libros/favoritos/', views.favorites, name='favorites'),
    
]
