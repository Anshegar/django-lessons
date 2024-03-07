from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse

from .models import News, Category
from .templates.news import *

# Create your views here.

def index_handmade(request):
    news = News.objects.all()
    res = '<h1>Список Новостей</h1>'
    for i in news:
        res += f'<div>\n<p>{i.title}</p>\n<p>{i.content}</p>\n</div>\n<hr>\n'
    print('--- request query', request)
    return HttpResponse(res)

def test(request):
    return HttpResponse('<h1>Test page</h1>')




def index(request):
    news = News.objects.all()
    context = {"news_in_t":news,
               "title":'Список Новостей',
               }
    return render( request, 'news/index.html', context )


def get_category(request, category_id):
    news = News.objects.filter(category_id = category_id)
    categories1 = Category.objects.all()
    category = Category.objects.get(id=category_id)

    context = {"news":news, 
               "category":category,
                "categories1":categories1 }

    return render( request, 'news/category.html', context )


def view_news(request,news_id):
    #news_item = News.objects.get(id = news_id)
    news_item = get_object_or_404(News, id = news_id)
    context = {'news_item':news_item,
               }
    return render(request, 'news/view_news.html', context)