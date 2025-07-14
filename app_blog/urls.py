from django.urls import path
from . import views
from .views import (
    login_view, logout_view, register_view,
    index, CrearPostView, CrearComentarioView,
    buscar_post, detalle_post, quienes_somos
)



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.register_view, name='registro'),
    path('crear_post/', CrearPostView.as_view(), name='crear_post'),
    path('crear_comentario/', CrearComentarioView.as_view(), name='crear_comentario'),
    path('buscar_post/', views.buscar_post, name='buscar_post'),
    path('post/<int:post_id>/', views.detalle_post, name='detalle_post'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password_view, name='cambiar_password'),
    path('', views.index, name='inicio'),  
    path('post/<int:post_id>/editar/', views.editar_post, name='editar_post'),
    path('post/<int:post_id>/borrar/', views.borrar_post, name='borrar_post'),
    path('quienes-somos/', quienes_somos, name='quienes_somos'),

]
    