# Create your API views here.

from .serializers import NewsSerializer
from .serializers import NewsModelSerializer
from .serializers import encode
from .serializers import NewsModelSerializer_DB

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import * 
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


from django.forms import model_to_dict

from .models import News, Category

class NewsModelAPIView_DB(APIView):
    def get(self, request):
        #my_ser = NewsModelSerializer_DB()
        #return Response( {"posts":my_ser.encode_to_get()})
        news = News.objects.all()
        return Response({"posts": NewsModelSerializer_DB(news, many=True).data})
    
    def post(self, request):
        serializer = NewsModelSerializer_DB(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

        # new_news = News.objects.create(
        #     title           = request.data['title'],
        #     content         = request.data['content'],
        #     is_published    = request.data['is_published'],
        #     category_id     = request.data['category_id'],
        # ) 
        #return Response({'post':NewsModelSerializer_DB(new_news).data})   # Вернем JSON строку сформированную по переданным данным

    def put(self, request, *args, **kwargs):
        # ВАЖНО: Если ключ аргумент-поиска ОБЪЕКТА (в данном случае id) не указан в URL запросе то :
        id = kwargs.get("id", None) # Проверка наличия данных по ключу id иначе ставим None
        if not id:                  # Если  ключа нет - id == None, райзим ошибку
            return Response({"error": "Method PUT not allowed"})
        
        # Пробуем получить Объект по заданному в URL запросе аргументу , с проверкой ошибок
        try:
            instance = News.objects.get(id = id)
        except Exception as e:
            return Response({"error": "Object dose not exist"})  
        
        # Данные которые хотим изменить и данные на которые меняем
        # --- в сериализаторе потому что вызовется def update(self, instance, validated_data) с 2-мя аргументами
        serializer = NewsModelSerializer_DB(data=request.data, instance=instance)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})
    
    def delete(self, request, *args, **kwargs):
        # ВАЖНО: Если ключ аргумент-поиска ОБЪЕКТА (в данном случае id) не указан в URL запросе то :
        id = kwargs.get("id", None) # Проверка наличия данных по ключу id иначе ставим None
        if not id:                  # Если  ключа нет - id == None, райзим ошибку
            return Response({"error": "Method DELETE not allowed"})
        
        # Пробуем получить Объект по заданному в URL запросе аргументу , с проверкой ошибок
        try:
            instance = News.objects.get(id = id)
        except Exception as e:
            return Response({"error": "Object dose not exist"})

        News.objects.get(id = id ).delete() 
        
        return Response({"post":"Запись " + str(id) + " удалена"})


class NewsModelAPIView(APIView):
    def get(self, request):
        my_ser = NewsModelSerializer()
        return Response(my_ser.encode_to_get())
    
    def post(self, request):
        my_ser = NewsModelSerializer()
        parse = my_ser.decode(request.data)
        return Response({'post':parse}) 
    
    # def post(self, request):
    #     my_ser = NewsModelSerializer()
    #     parse = my_ser.decode_from_post(request.data)
    #     return Response({'post':parse}) 


# Собственный сериализатор через функцию
# class NewsModelAPIView(APIView):
#     def get(self, request):
#         return Response(encode())



# API Без Сериализатора
class NewsAPIViewNoSerializer(APIView):
    def get(self, request):                 # request содержит все параметры входящего GET запроса
        data = News.objects.all().select_related('category').values()
        queryset = News.objects.all().select_related('category')
        print([i.category.title for i in queryset])
        return Response({'Objects':list(data),'Category title': list([i.category.title for i in queryset])})   
    # Вернем JSON строку сформированную по .values

    def post(self, request):            # request содержит все параметры входящего GET запроса
        print('Идет обработка полученных данных')
        new_news = News.objects.create(
            title           = request.data['title'],
            content         = request.data['content'],
            is_published    = request.data['is_published'],
            category_id     = request.data['category_id'],
        )

        #from django.forms import model_to_dict
        #return Response({'post': model_to_dict(new_news)})  
        data = News.objects.filter(title = new_news.title).select_related('category').values()
        return Response({'post':list(data)})   # Вернем JSON строку сформированную по .values









# DRF API GENERIC QUERYSET списка
class NewsAPIView(generics.ListAPIView):
    queryset = News.objects.all()           # Список из какой Модели будет передаваться в API
    serializer_class = NewsSerializer       # Указать класс- сериализатор(подгоняет данные под нужный формат)

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})

    def put(self, request, *args, **kwargs):
        # ВАЖНО: Если ключ аргумент-поиска ОБЪЕКТА (в данном случае id) не указан в URL запросе то :
        id = kwargs.get("id", None) # Проверка наличия данных по ключу id иначе ставим None
        if not id:                  # Если  ключа нет - id == None, райзим ошибку
            return Response({"error": "Method PUT not allowed"})
        
        # Пробуем получить Объект по заданному в URL запросе аргументу , с проверкой ошибок
        try:
            instance = News.objects.get(id = id)
        except Exception as e:
            return Response({"error": "Object dose not exist"})  
        
        # Данные которые хотим изменить и данные на которые меняем
        # --- в сериализаторе потому что вызовется def update(self, instance, validated_data) с 2-мя аргументами
        serializer = NewsSerializer(data=request.data, instance=instance)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post':serializer.data})
    
    def delete(self, request, *args, **kwargs):
        # ВАЖНО: Если ключ аргумент-поиска ОБЪЕКТА (в данном случае id) не указан в URL запросе то :
        id = kwargs.get("id", None) # Проверка наличия данных по ключу id иначе ставим None
        if not id:                  # Если  ключа нет - id == None, райзим ошибку
            return Response({"error": "Method DELETE not allowed"})
        
        # Пробуем получить Объект по заданному в URL запросе аргументу , с проверкой ошибок
        try:
            instance = News.objects.get(id = id)
        except Exception as e:
            return Response({"error": "Object dose not exist"})

        News.objects.get(id = id ).delete() 
        
        return Response({"post":"Запись " + str(id) + " удалена"})


class NewsAPIListPagination(PageNumberPagination):  # Класс пагинации имеет приоритет перед ГЛОБАЛЬНЫМИ настройками
    page_size = 2                              # Количество записей на страницу
    page_size_query_param = 'page_size'        # Доп параметрт для GET запроса в URL строке, сколько записей получить 
    max_page_size = 1000                       # НО page_size не может быть больше значения max_page_size
# .../api/v1/newsapilist/?page=3&page_size=4   # Выведет не 2 а 4 записи

class NewsAPIList(generics.ListCreateAPIView):  # - GET + POST - Чтение данных по GET запросу и создание из них списка по POST запросу
    queryset = News.objects.all()               # READ      Создаем QUERYSET запрос для возвращения клиенту
    serializer_class = NewsSerializer           # CREATE    Указать класс- сериализатор(подгоняет данные под нужный формат и Модель)
    permission_classes = (IsAuthenticatedOrReadOnly,)   # Указываем коллекцию допусков
    pagination_class = NewsAPIListPagination    # Класс пагинации для этого API представления


class NewsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()               # READ      Создаем QUERYSET запрос для возвращения клиенту
    serializer_class = NewsSerializer           # UPDATE    Указать класс- сериализатор(подгоняет данные под нужный формат и Модель)
    permission_classes = (IsOwnerOrReadOnly,)   # Указываем коллекцию допусков

class NewsAPIRetrDestroy(generics.RetrieveDestroyAPIView ):  
    queryset = News.objects.all()               # READ      Создаем QUERYSET запрос для возвращения клиенту
    serializer_class = NewsSerializer           # DELETE
    permission_classes = (IsAdminOrReadOnly,)   # Указываем коллекцию допусков

class NewsAPIFullCRUD(generics.RetrieveUpdateDestroyAPIView):   # GET \\ PUT \\ PATCH \\DELETE
    queryset = News.objects.all()                   # READ      Создаем QUERYSET запрос для возвращения клиенту
    serializer_class = NewsSerializer               # UPDATE    Указать класс- сериализатор(подгоняет данные под нужный формат и Модель)
    permission_classes = (IsAuthenticated,)         # Указываем коллекцию допусков
    authentication_classes = (TokenAuthentication,) # Тип Аутентефикации требуемой для данного представления



class NewsJWTTokenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = News.objects.all()               # READ      Создаем QUERYSET запрос для возвращения клиенту
    serializer_class = NewsSerializer           # UPDATE    Указать класс- сериализатор(подгоняет данные под нужный формат и Модель)
    permission_classes = (IsAuthenticated,)     # Указываем коллекцию допусков
    #authentication_classes =                   # Быть не должно иначе через Djoser 



# Альтернатива написанию кучи отдельных views наследуемых от generics.
class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()              
    serializer_class = NewsSerializer 

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return News.objects.all()[:3]  
        return News.objects.filter(id = pk)
    

    @action(methods = ["GET"], detail = False) #(detail = False -  для возврата списка \\ detail = True - для возврата 1 конкретной записи)
    def category(self,request):
        cats= Category.objects.all()
        return Response({"cats":[c.title for c in cats]})
    
    @action(methods = ["GET"], detail = True) 
    def category_id(self,request, pk = None):
        cats= Category.objects.get(id = pk)
        return Response({"cats":cats.title})