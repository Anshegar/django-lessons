from django.contrib import admin

# Register your models here.

from .models import News, Category



# Класс-редактор для News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id','title','category','create_at','update_at','is_published',)
    list_display_links = ('id','title',)
    search_fields = ('title','content')
    list_editable = ('is_published',)
    list_filter = ('is_published','category',)

# Класс-редактор для категорий отдающих данные на Foreign Key в News
class NewsCategory(admin.ModelAdmin):
    list_display = ('id','title',)
    list_display_links = ('id','title',)
    search_fields = ('title',)

admin.site.register(News,NewsAdmin)
admin.site.register(Category,NewsCategory)
