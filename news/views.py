from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from django.http import HttpResponse

from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView

from .models import News, Category
from .templates.news import *

from .forms import NewsForm, UserRegisterForm

from .utils import MyMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import UseLoginForm
from .forms import ContactForm
from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail, send_mass_mail

# Create your views here.


def contact(request):
    if request.method != 'POST':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(form.cleaned_data['subject'],form.cleaned_data['content'],
                                'oloo@mail.ru', ['woloo@mail.ru'],fail_silently=False,)
            # Проверка отправлено письмо или нет
            if mail:
                messages.success(request, "Mail Sended!")
                return redirect("contact")
            else:
                messages.success(request, "Mail Not Sended!")
    context = {"form":form,}
    return render(request, 'news/test.html', context)


def test(request):
    if request.method != 'POST':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(form.cleaned_data['subject'],form.cleaned_data['content'],
                                'oloo@mail.ru', ['woloo@mail.ru'],fail_silently=False,)
            # Проверка отправлено письмо или нет
            if mail:
                messages.success(request, "Mail Sended!")
                return redirect("test")
            else:
                messages.success(request, "Mail Not Sended!")
    context = {"form":form,}
    return render(request, 'news/test_orig.html', context)


def user_login(request):
    if request.method != 'POST':
        form = UseLoginForm()
    else:
        form = UseLoginForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы Вошли!")
            return redirect("home")
        else:
            messages.error(request, "Неправильно введены данные пользователя.")
    context ={"form": form}
    return render(request, 'news/login.html', context)



def user_logout(request):
    logout(request)
    return redirect("home")



def register(request):
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # form.save()               # Без авто логина
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            # return redirect("login")  # Если без автологина 
            return redirect("home")
        else:
            messages.error(request, "Ошибка Регистрации")
    context ={"form": form}
    return render(request, 'news/register.html', context)






# def test(request):
#     objects = ["john", "paul", "george", "ringo","john2", "paul2", "george2", "ringo2","john3", "paul3", "george3", "ringo3",]
#     paginator = Paginator(objects, 2)

#     page_number = request.GET.get("page",1)     # Получаем Номер страницы (в это то чему равен page URL page=)
#     # --- Если get("page") найден не будет то автоматом поставит номер страницы 1 (а дальше сам будет прибавлять)
#     page_obj = paginator.get_page(page_number)  # Создаем Объект page_obj для Шаблона]

#     context = {"page_obj": page_obj}
#     return render(request, "news/test.html", context)



class HomeNews(MyMixin, ListView):
    model  = News                               # = News.objects.all()    - определяем из какой МОДЕЛИ мы будем забирать данные 
    template_name = "news/home_news_list.html"  # путь до Шаблона и его имя
    context_object_name = "news"                # Название Объекта передаваемого из Python в Шаблон
    #extra_context = {"title":"Главная"}         # Доп данные передаваемые в Шаблон (ТОЛЬКО ДЛЯ {{СТАТИЧНЫХ}} данных)
    #allow_empty =False
    #queryset = News.objects.filter(is_published=True).select_related('category')
    mixin_prop = 'Hello world'
    paginate_by = 2
    
    # Переопределение метода для передачи Списков и прочих данных
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)            # Сохраняем исходные данные (заданные выше model, template_name и т.д. )
        context["title"] = self.get_upper("Главная страница")                   # Дополняем данные тем что нам надо
        context["mixin_prop"] = self.get_prop
        return context
    
    # Фильтр данных ( а ля news = News.objects.filter(is_published=True) + связь с категориями)
    def get_queryset(self) -> QuerySet[Any]:
        return News.objects.filter(is_published=True).select_related('category')




class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = "news/home_news_list.html"
    context_object_name = "news"
    allow_empty =False
    paginate_by = 2

    
    # Фильтр данных привязка к передаваемому значению <int:category_id> , он УЖЕ есть в экземпляре self
    def get_queryset(self) -> QuerySet[Any]:
        return News.objects.filter(category_id=self.kwargs["category_id"],is_published=True).select_related('category')

        # Переопределение метода для передачи Списков и прочих данных
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)            # Сохраняем исходные данные (заданные выше model, template_name и т.д. )
        context["title"] = self.get_upper(Category.objects.get(id =self.kwargs["category_id"]))   # Меняем заголовок на тот что соответствует динамическому номеру
        return context
    



class ViewNews(DetailView):
    model  = News                               # = News.objects.all()    - определяем из какой МОДЕЛИ мы будем забирать данные 
    # pk_url_kwarg = 'news_id'                  # pk он же id  int переменная
    # slug_url_kwarg =                          # slug         str переменная
    template_name = "news/news_detail.html"     # Путь к шаблону
    context_object_name = 'news_item'           # Передаваемый Объект




class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm                       # = News.objects.all()    - определяем класс ФОРМЫ c которой связываем
    template_name = "news/add_news.html"        # Путь к шаблону
    #success_url =                              # Куда Редиректить после создания объекта, если не указано, то в модели надо создать get_absolute_url иначе будет ошибка редиректа
    #success_url = '/'                          # Статичный редирект адрес  
    #success_url = reverse_lazy("home",)        # Динамический редирект (он лучше)
    login_url = "/admin/"                       # Если пользователь не авторизован (from django.contrib.auth.mixins import LoginRequiredMixin)






def index_handmade(request):
    news = News.objects.all()
    res = '<h1>Список Новостей</h1>'
    for i in news:
        res += f'<div>\n<p>{i.title}</p>\n<p>{i.content}</p>\n</div>\n<hr>\n'
    print('--- request query', request)
    return HttpResponse(res)





def index(request):
    #news = News.objects.all()
    news = News.objects.filter(is_published=True)
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


# def add_news(request):
#     if request.method != 'POST':
#         form = NewsForm()
#     else:
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             news = form.save()
#             #return redirect("home")
#             return redirect (news)

#     context = {"form":form,}
#     return render(request, 'news/add_news.html', context)



# def add_news(request):
#     if request.method != 'POST':
#         form = NewsForm()
#     else:
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             news = News.objects.create(**form.cleaned_data)
#             #News.objects.create(title =form.cleaned_data["title"], content =form.cleaned_data["content"], is_published =form.cleaned_data["is_published"],category =form.cleaned_data["category"], )
#             #return redirect("home")
#             return redirect (news)

#     context = {"form":form,}
#     return render(request, 'news/add_news.html', context)