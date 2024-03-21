from django.db import models
from django.urls import reverse, reverse_lazy


# Create your models here.

class News(models.Model):
    id = models.BigAutoField(primary_key = True) # Если не указать, то проставит автоматически
    title = models.CharField(max_length=150, verbose_name = 'Наименование')
    content = models.TextField(blank = True, verbose_name = 'Контент')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата Публикации')
    update_at = models.DateTimeField(auto_now=True, verbose_name = 'Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name = 'Фото',blank=True)
    is_published= models.BooleanField(default = True, verbose_name = 'Опубликовано')
    category = models.ForeignKey('Category', on_delete = models.PROTECT,  verbose_name = 'Категория')
    views = models.IntegerField(default = 0)


    def get_absolute_url(self):
        #return reverse("view_news", kwargs={"news_id": self.id})
        return reverse("view_news", kwargs={"pk": self.id})

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-create_at','title']


class Category(models.Model):
    id = models.BigAutoField(primary_key=True) # Если не указать, то проставит автоматически
    title = models.CharField(max_length = 150, db_index = True, verbose_name = 'Наименование категории')


    def get_absolute_url(self):
       return reverse("category", kwargs={"category_id": self.id})

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
