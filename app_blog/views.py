from django.shortcuts import render, redirect
from .models import Autor, Post, Comentario
from .forms import AutorForm, PostForm, ComentarioForm, BuscarPostForm

def index(request):
    posts = Post.objects.all().order_by('-fecha_publicacion')
    return render(request, 'app_blog/index.html', {'posts': posts})

def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'app_blog/post_list.html', {'posts': posts})

def crear_autor(request):
    form = AutorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inicio')
    return render(request, 'app_blog/crear_autor.html', {'form': form})

def crear_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('inicio')
    return render(request, 'app_blog/crear_post.html', {'form': form})

def crear_comentario(request):
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = ComentarioForm()
    return render(request, 'app_blog/crear_comentario.html', {'form': form})

def buscar_post(request):
    form = BuscarPostForm(request.GET or None)
    posts = []
    if form.is_valid():
        titulo = form.cleaned_data['titulo']
        posts = Post.objects.filter(titulo__icontains=titulo)
    return render(request, 'app_blog/buscar_post.html', {'form': form, 'posts': posts})

def detalle_post(request, post_id):
    post = Post.objects.get(id=post_id)
    comentarios = Comentario.objects.filter(post=post)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post  # asignar post actual
            comentario.save()
            return redirect('detalle_post', post_id=post.id)
    else:
        form = ComentarioForm()

    return render(request, 'app_blog/detalle_post.html', {
        'post': post,
        'comentarios': comentarios,
        'form': form,
    })