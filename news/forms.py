from django import forms
from .models import Category, News # Что  бы при добавлении новости сделать выпадающий список к какой категории относится эта новость

from django.core.exceptions import ValidationError

import re

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import CaptchaField
from captcha.fields import CaptchaTextInput

class ContactForm(forms.Form):
    subject = forms.CharField(label="Тема", help_text="Подсказка темы", widget= forms.TextInput(attrs={"class":"form-control"}))
    content = forms.CharField(label="Текст письма", widget= forms.Textarea(attrs={"class":"form-control","row":5}, ))
    captcha = CaptchaField()


class UseLoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя", help_text="Подсказка для поля username",widget= forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label="Пароль", widget= forms.PasswordInput(attrs={"class":"form-control"}))

# Создаем класс формы Регистрации
# Объявляем поля для формы
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", help_text="Подсказка для поля username",widget= forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(label="Пароль", widget= forms.PasswordInput(attrs={"class":"form-control"}))
    password2 = forms.CharField(label="Подтверждение Пароля", widget= forms.PasswordInput(attrs={"class":"form-control"}))
    email = forms.EmailField(label="Email", widget= forms.EmailInput(attrs={"class":"form-control"}) )
    captcha = CaptchaField()

    class Meta():
        model = User
        fields = ["username", "email", "password1", "password2",]
    #     widgets =   {"username" : forms.TextInput(attrs={"class":"form-control"}),
    #                  "email" : forms.EmailInput(attrs={"class":"form-control", }),
    #                  "password1" : forms.PasswordInput(attrs={"class":"form-control"}),
    #                  "password2" : forms.PasswordInput(attrs={"class":"form-control"}),
    #                 }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title','content','is_published','category',]
        widgets =   {"title" : forms.TextInput(attrs={"class":"form-control"}),
                     "content" : forms.Textarea(attrs={"class":"form-control", "rows":"5"}),
                     "category" : forms.Select(attrs={"class":"form-control"}),

                    }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if re.match(r"\d", title):
            raise ValidationError(" Название не должно начинаться цифры")
        return title

class NewsForm_notDB(forms.Form):
    title = forms.CharField(max_length=150, label="Название", widget=forms.TextInput(attrs={"class":"form-control"})) # Текстовое поле
    content = forms.CharField(label="Текст", required= False, widget=forms.Textarea(attrs={"class":"form-control", "rows":"5"}))                 # Текстовое поле
    is_published = forms.BooleanField(label="Опубликовано?", initial=True,)    # ЧекБокс
    category = forms.ModelChoiceField(empty_label="Выберете категорию" ,label="Категория",queryset=Category.objects.all(), widget=forms.Select(attrs={"class":"form-control"}))    
    # Выпадающий список - ПРОСТОЙ - ChoiceField - или  СВЯЗАННЫЙ С ForeignHey МОДЕЛИ - ModelChoiceField(или ModelMultipleChoiceField )
    # --- с обязательным атрибутом - queryset - указывающим с какой моделью связь 