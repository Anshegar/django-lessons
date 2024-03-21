from django.contrib import admin

# Register your models here.

from .models import News, Category

from django.utils.safestring import mark_safe

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = News
        fields = '__all__'



# Класс-редактор для News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','create_at','update_at','is_published','get_photo')
    list_display_links = ('id','title',)
    search_fields = ('title','content')
    list_editable = ('is_published',)
    list_filter = ('is_published','category',)
    fields = ('title','category', 'content', 'photo', 'get_photo', 'is_published', 'views','create_at','update_at',)
    readonly_fields = ('get_photo', 'views','create_at','update_at',)
    save_on_top = True
    form = PostAdminForm


    def get_photo(self,obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50">')  # Помечает данную строку как html код и никак её не экранирует
        else:
            return "Изображение отсутствует"
        
    get_photo.short_description = "Миниатюра"

# Класс-редактор для категорий отдающих данные на Foreign Key в News
class NewsCategory(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id','title',)
    search_fields = ('title',)

admin.site.register(News,NewsAdmin)
admin.site.register(Category,NewsCategory)


admin.site.site_header = 'Ololo'
admin.site.site_title = 'Wololo'