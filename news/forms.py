from django import forms
from .models import Category, News # Что  бы при добавлении новости сделать выпадающий список к какой категории относится эта новость


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title','content','is_published','category',]
        widgets =   {"title" : forms.TextInput(attrs={"class":"form-control"}),
                     "content" : forms.Textarea(attrs={"class":"form-control", "rows":"5"}),
                     "category" : forms.Select(attrs={"class":"form-control"}),

                    }


class NewsForm_notDB(forms.Form):
    title = forms.CharField(max_length=150, label="Название", widget=forms.TextInput(attrs={"class":"form-control"})) # Текстовое поле
    content = forms.CharField(label="Текст", required= False, widget=forms.Textarea(attrs={"class":"form-control", "rows":"5"}))                 # Текстовое поле
    is_published = forms.BooleanField(label="Опубликовано?", initial=True,)    # ЧекБокс
    category = forms.ModelChoiceField(empty_label="Выберете категорию" ,label="Категория",queryset=Category.objects.all(), widget=forms.Select(attrs={"class":"form-control"}))    
    # Выпадающий список - ПРОСТОЙ - ChoiceField - или  СВЯЗАННЫЙ С ForeignHey МОДЕЛИ - ModelChoiceField(или ModelMultipleChoiceField )
    # --- с обязательным атрибутом - queryset - указывающим с какой моделью связь 