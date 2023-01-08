from django.urls import path
from . import views

urlpatterns = [
    path('', views.administrar, name='administrar'),
    #solicitudes
    path('solicitudes/', views.list_requests, name='solicitudes'),
    path('solicitud/<int:user_id>/<username>/', views.crearSolicitud, name='crear_solicitud'),
    path('solicitud/eliminar/<int:solicitud_id>/<int:user_id>/<username>/', views.delete_request, name='delete_request'),
    path('solicitud/aceptar/<int:user_id>/<username>/', views.accept_request, name='accept_request'),
    #libros
    path('libros/subir-libros/', views.upload_book, name='upload_book'),
    path('libros/subir-libro/fisico/', views.upload_bookF, name='upload_bookF'),
    path('libros/subir-libro/digital/', views.upload_bookD, name='upload_bookD'),
    path('libros/editar/lista/', views.edit_books, name='edit_books'),
    path('libros/editar/f/<int:book_id>/<slug:book_slug>/', views.edit_bookF, name='edit_bookF'),
    path('libros/editar/d/<int:book_id>/<slug:book_slug>/', views.edit_bookD, name='edit_bookD'),
    #comentarios
    path('libros/comentarios/lista-de-libros/', views.list_pc, name='list_pc'),
    path('libros/comentarios/libro/<type>/<int:book_id>/<slug:book_slug>/', views.list_comments, name='list_comments'),
    path('libros/comentarios/eliminar/<type>/<int:comment_id>/', views.delete_comment, name='delete_comment'),

]