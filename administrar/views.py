from django.shortcuts import render, get_object_or_404, redirect
from biblioteca.models import *
from account.models import *
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Count
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from biblioteca.forms import *

@login_required
@permission_required('administrar.delete_solicitud', login_url='home')
def administrar(request):
    return render(request, 'administrar/administrar.html')

def crearSolicitud(request, user_id, username):
    user = get_object_or_404(User, id=user_id, username=username)
    Solicitud.objects.create(user=user)
    return redirect(reverse('profile', args=[user.id, user]))

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def delete_request(request, solicitud_id, user_id, username):
    user = get_object_or_404(User, username=username, id=user_id)
    solicitud = get_object_or_404(Solicitud, user=user, id=solicitud_id)
    solicitud.delete()
    return redirect(reverse('solicitudes'))    

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def accept_request(request, user_id, username):
    user = get_object_or_404(User, username=username, id=user_id)
    solicitud = get_object_or_404(Solicitud, user=user)
    solicitud.delete()
    group = Group.objects.get(name='Administrador')
    user.groups.add(group)
    user.profile.administrador = True
    user.profile.save()
    return redirect(reverse('solicitudes'))    

@permission_required('administrar.view_solicitud', login_url='home')
@login_required
def list_requests(request):
    # print(request.user.get_group_permissions())
    solicitudes = Solicitud.objects.all().order_by('-creado')
    paginator = Paginator(solicitudes, 6)
    page_number = request.GET.get('pagina', 1)
    try: solicitudes = paginator.page(page_number)
    except PageNotAnInteger: solicitudes = paginator.page(1)
    except EmptyPage: solicitudes = paginator.page(paginator.num_pages)
    context = {'solicitudes':solicitudes,}
    return render(request, 'administrar/solicitudes.html', context)

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def upload_book(request): return render(request, 'administrar/libros/subir.html')

@permission_required('biblioteca.add_fisico', login_url='home')
@login_required
def upload_bookF(request):
    if request.method == 'POST':
        form = UploadBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
    else:
        form = UploadBookForm()
    return render(request, 'administrar/libros/formulario.html', {'form':form,})

@permission_required('biblioteca.add_fisico', login_url='home')
@login_required
def upload_bookD(request):
    if request.method == 'POST':
        form = UploadEBookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
    else:
        form = UploadEBookForm()
    return render(request, 'administrar/libros/formulario.html', {'form':form,})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def edit_books(request):
    query = request.GET.get('query')
    if query !=None:
        dg = Fisico.objects.filter(descripcion__contains=query, titulo__contains=query)
        fs = Digital.objects.filter(descripcion__contains=query, titulo__contains=query)
    else:
        dg = Digital.objects.all()
        fs = Fisico.objects.all() #list(chain(dg, fs))
    books = sorted(chain(dg, fs), key=attrgetter('creado'))
    paginator = Paginator(books, 6)
    page_number = request.GET.get('pagina', 1)
    try: books = paginator.page(page_number)
    except PageNotAnInteger: books = paginator.page(1)
    except EmptyPage: books = paginator.page(paginator.num_pages)
    
    return render(request, 'administrar/libros/lista.html', {'books':books})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def edit_bookF(request, book_id, book_slug):
    book = get_object_or_404(Fisico, id=book_id, slug=book_slug)
    if request.method == 'POST':
        form = UploadBookForm(instance=book, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()   
            return redirect('home')
    else:
        form = UploadBookForm(instance=book)
    return render(request, 'administrar/libros/editar.html', {'form':form,'book':book})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def edit_bookD(request, book_id, book_slug):
    book = get_object_or_404(Digital, id=book_id, slug=book_slug)
    if request.method == 'POST':
        form = UploadEBookForm(instance=book, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()   
    else:
        form = UploadEBookForm(instance=book)
    return render(request, 'administrar/libros/editar.html', {'form':form,'book':book})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def list_pc(request):
    query = request.GET.get('query')
    if query !=None:
        dg = Fisico.objects.filter(descripcion__contains=query, titulo__contains=query)
        fs = Digital.objects.filter(descripcion__contains=query, titulo__contains=query)
    else:
        dg = Digital.objects.all()
        fs = Fisico.objects.all() #list(chain(dg, fs))
        
    books = sorted(chain(dg, fs), key=attrgetter('creado'))
    paginator = Paginator(books, 6)
    page_number = request.GET.get('pagina', 1)
    try: books = paginator.page(page_number)
    except PageNotAnInteger: books = paginator.page(1)
    except EmptyPage: books = paginator.page(paginator.num_pages)
    
    return render(request, 'administrar/comentarios/lista_pc.html', {'books':books,})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def list_comments(request, type, book_id, book_slug):
    query = request.GET.get('query')
    if type=='f':
        book = get_object_or_404(Fisico, slug=book_slug, id=book_id)
        comments = book.fcomments.all()
    else:
        book = get_object_or_404(Digital, slug=book_slug, id=book_id)
        comments = book.dcomments.all()
    
    if query!=None:comments.filter(cuerpo__contains=query)
    
    paginator = Paginator(comments, 6)
    page_number = request.GET.get('pagina', 1)
    try: comments = paginator.page(page_number)
    except PageNotAnInteger: comments = paginator.page(1)
    except EmptyPage: comments = paginator.page(paginator.num_pages)
    
    return render(request, 'administrar/comentarios/comentarios.html', {'comments':comments, 'book': book, 'type':type,})

@permission_required('administrar.delete_solicitud', login_url='home')
@login_required
def delete_comment(request, type, comment_id):
    if type=='f':comment = get_object_or_404(Comentario_f, id=comment_id)
    else:comment = get_object_or_404(Comentario_d, id=comment_id)
    book = comment.book
    comment.delete()
    return redirect(reverse('list_comments', args=[type, book.id, book.slug]))        