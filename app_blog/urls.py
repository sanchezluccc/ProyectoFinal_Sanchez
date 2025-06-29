from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('nuevo_autor/', views.crear_autor, name='crear_autor'),
    path('nuevo_post/', views.crear_post, name='crear_post'),
    path('nuevo_comentario/', views.crear_comentario, name='crear_comentario'),
    path('buscar/', views.buscar_post, name='buscar_post'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),


]
    