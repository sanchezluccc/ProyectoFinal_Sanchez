from django.contrib.auth.models import User
from django.db import models



class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.autor.username} en {self.post.titulo}"
    
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    fecha_cumpleaños = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)
    else:
       
        try:
            instance.perfil.save()
        except Perfil.DoesNotExist:
           
            Perfil.objects.create(usuario=instance)