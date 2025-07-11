from django.shortcuts import render, redirect,  get_object_or_404
from .models import  Post, Comentario
from .forms import  PostForm, ComentarioForm, BuscarPostForm, RegistroForm
from django.contrib.auth.decorators import login_required

def index(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'app_blog/index.html', {'posts': posts})

def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'app_blog/post_list.html', {'posts': posts})


from django.views import View
from django.shortcuts import render, redirect
from .forms import PostForm
from .mixins import LoginRequiredMessageMixin

class CrearPostView(LoginRequiredMessageMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'app_blog/crear_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('inicio')
        return render(request, 'app_blog/crear_post.html', {'form': form})


from django.views import View
from django.shortcuts import redirect
from .forms import ComentarioForm
from .mixins import LoginRequiredMessageMixin

class CrearComentarioView(LoginRequiredMessageMixin, View):
    def post(self, request):
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.save()
        return redirect('inicio')

def buscar_post(request):
    form = BuscarPostForm(request.GET or None)
    posts = []
    if form.is_valid():
        titulo = form.cleaned_data['titulo']
        posts = Post.objects.filter(titulo__icontains=titulo)
    return render(request, 'app_blog/buscar_post.html', {'form': form, 'posts': posts})

def detalle_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=post).order_by('-fecha')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.autor = request.user
                comentario.post = post
                comentario.save()
                return redirect('detalle_post', post_id=post.id)
        else:
            return redirect('login')  
    else:
        form = ComentarioForm()

    return render(request, 'app_blog/detalle_post.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form
    })

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  
    else:
        form = AuthenticationForm()
    return render(request, 'app_blog/login.html', {'form': form})

# Vista de logout
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  

# Vista de registro
def register_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ahora podés iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor corregí los errores abajo.")
    else:
        form = RegistroForm()
    return render(request, 'app_blog/registro.html', {'form': form})

from .forms import LoginForm  
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  
    else:
        form = LoginForm()  
    return render(request, 'app_blog/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PerfilForm, EditarUsuarioForm, CambiarPasswordForm

@login_required
def perfil_view(request):
    return render(request, 'app_blog/perfil.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EditarUsuarioForm, PerfilForm

@login_required
def editar_perfil_view(request):
    usuario = request.user
    perfil = usuario.perfil

    if request.method == 'POST':
        user_form = EditarUsuarioForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return redirect('perfil')
    else:
        user_form = EditarUsuarioForm(instance=usuario)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'app_blog/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import CambiarPasswordForm

@login_required
def cambiar_password_view(request):
    if request.method == 'POST':
        form = CambiarPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión iniciada
            return redirect('perfil')  # o donde quieras redirigir
    else:
        form = CambiarPasswordForm(user=request.user)
    return render(request, 'app_blog/cambiar_password.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import PostForm
from .models import Post

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Verificar que el usuario sea el autor
    if post.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para editar este post.")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('detalle_post', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'app_blog/editar_post.html', {'form': form, 'post': post})


@login_required
def borrar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Verificar que el usuario sea el autor
    if post.autor != request.user:
        return HttpResponseForbidden("No tienes permiso para borrar este post.")

    if request.method == "POST":
        post.delete()
        return redirect('inicio')

    return render(request, 'app_blog/confirmar_borrado.html', {'post': post})
