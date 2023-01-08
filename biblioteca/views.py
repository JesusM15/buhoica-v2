from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Count

def homePage(request, ordenar='creado'):
    query = request.GET.get('query')
    if query != None:
        dg = Fisico.objects.filter(descripcion__contains=query, titulo__contains=query)
        fs = Digital.objects.filter(descripcion__contains=query, titulo__contains=query)
    else:
        dg = Digital.objects.all()
        fs = Fisico.objects.all() #list(chain(dg, fs))
    books = sorted(chain(dg, fs), key=attrgetter(ordenar))

    paginator = Paginator(books, 6)
    page_number = request.GET.get('pagina', 1)
    try: books = paginator.page(page_number)
    except PageNotAnInteger: books = paginator.page(1)
    except EmptyPage: books = paginator.page(paginator.num_pages)
    context = {'books':books, 'bottom':True, 'section':True,}
    
    return render(request, 'biblioteca/index.html', context)

def detail_pageF(request, book_slug, creado):
    book = get_object_or_404(Fisico, slug=book_slug, creado=creado)
    book_similar_ids = book.tags.values_list('id', flat=True)
    similar_books = Fisico.objects.filter(tags__in=book_similar_ids).exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')).order_by('-same_tags')[:3]
    comments = book.fcomments.all().order_by('-creado')
    form = CommentFormFisico()
    context = {'book':book, 'similar_books':similar_books,'form':form,'comments':comments}
    return render(request, 'biblioteca/paginas/detail_fisico.html', context)
def detail_pageD(request, book_slug, creado):
    book = get_object_or_404(Digital, slug=book_slug, creado=creado)
    book_similar_ids = book.tags.values_list('id', flat=True)
    similar_books = Fisico.objects.filter(show=True, tags__in=book_similar_ids).exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags')).order_by('-same_tags')[:3]
    comments = book.dcomments.all().order_by('-creado')
    form = CommentFormFisico()
    context = {'book':book, 'similar_books':similar_books, 'form':form, 'comments':comments}
    return render(request, 'biblioteca/paginas/detail_digital.html', context)

@login_required
@require_POST
def like(request):
    book_id = request.POST.get('id')
    action = request.POST.get('action')
    tipo = request.POST.get('tipo')
    if book_id and action and tipo:
        try:
            if tipo=='f':
                book = Fisico.objects.get(id=book_id)
            elif tipo=='d': 
                book = Digital.objects.get(id=book_id)
                
            if action == 'like':
                book.users_likes.add(request.user)
            else:
                book.users_likes.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:pass
    return JsonResponse({'status':'error'})

@require_POST
@login_required
def book_comment(request, type, book_id, user):
    types = {'f':Fisico, 'd':Digital}
    usuario = get_object_or_404(User, username=user)
    book = get_object_or_404(types.get(type), id=book_id)
    comment = None
    if type == 'f': form = CommentFormFisico(data=request.POST)
    else: form = CommentFormDigital(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.book = book
        comment.user = usuario
        comment.save()
    return render(request, 'componentes/comment.html', {'book':book, 'user':user, 'form':form, 'comment':comment})

@login_required
def favorites(request):
    query = request.GET.get('query')
    if query != None:
        dg = request.user.digital_liked.filter(descripcion__contains=query, titulo__contains=query)
        fs = request.user.fisico_liked.filter(descripcion__contains=query, titulo__contains=query)
    else:
        dg = request.user.digital_liked.all()
        fs = request.user.fisico_liked.all() #list(chain(dg, fs))
    books = sorted(chain(dg, fs), key=attrgetter('titulo'))

    paginator = Paginator(books, 6)
    page_number = request.GET.get('pagina', 1)
    try: books = paginator.page(page_number)
    except PageNotAnInteger: books = paginator.page(1)
    except EmptyPage: books = paginator.page(paginator.num_pages)
    context = {'books':books,}
    
    return render(request, 'biblioteca/paginas/favoritos.html', context)