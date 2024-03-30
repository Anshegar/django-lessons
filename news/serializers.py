import io
from rest_framework import serializers 
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import *

# Класс Объекты Которого преобразуем в JSON строку
class NewsModel():

    def __init__(self,title, content) -> None:
        self.title      = title
        self.content    = content    




class NewsModelSerializer_DB(serializers.Serializer):
    title       = serializers.CharField(max_length=255)
    content     = serializers.CharField()
    create_at   = serializers.DateTimeField(read_only=True)
    update_at   = serializers.DateTimeField(read_only=True)
    is_published= serializers.BooleanField(default = True)
    category_id = serializers.IntegerField()

    def create(self, validated_data):           # validated_data приходит из post запроса  def post(self, request)
        #return super().create(validated_data)
        return News.objects.create(**validated_data)    
    
    def update(self, instance, validated_data):  # instance Объект Модели БД, validated_data так же из post     
                                                        # --- и являются словарем которые заменят данные в instance
        # Присваиваем данным поля значения данных пришедших из пост, А ЕСЛИ ИХ НЕТ, то оставляем их нетронутыми
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.create_at = validated_data.get("create_at", instance.create_at)
        instance.update_at = validated_data.get("update_at", instance.update_at)
        instance.is_published = validated_data.get("is_published", instance.is_published)
        instance.category_id = validated_data.get("category_id", instance.category_id)
        # Сохраняем Объект с новыми данными и возвращаем его для обработке во views - update откуда передан 
        instance.save()                                 
        return instance




    @staticmethod
    def encode_to_get():
        model = News.objects.all()
        model_sr = NewsModelSerializer_DB(model, many=True)
        serialized_data = model_sr.data
        return serialized_data
        #json = JSONRenderer().render(model_sr.data)
        #return json

    @staticmethod
    def decode_from_post(stream):
        serializer = NewsModelSerializer(data=stream)
        serializer.is_valid()
        return serializer.validated_data



# С Моделями напрямую не взаимодействует только с Объектами, так как Serializer а не ModelSerializer
class NewsModelSerializer(serializers.Serializer):
    # 1) Определяем чем серализатор должен обрабатывать ту или иную строку КЛАССА 
    title       = serializers.CharField(max_length=255)
    content     = serializers.CharField()

    @staticmethod
    def encode_to_get():
        # Создаем Объект Модели NewsModel
        model = NewsModel("News 666", "Контент: Тестируем ручной сериализатор")
        # Объект сериализации - Обрабатываем Объект, model, нашим ручным сериализатором NewsModelSerializer
        model_sr = NewsModelSerializer(model)
        # Вывод результата при помощи атрибута .data - это Сериализованые данные
        print(model_sr.data, type(model_sr.data), sep='\n')
        # Создаем JSON строку
        json = JSONRenderer().render(model_sr.data)
        print(json.decode('utf-8'))
        print(json)
        return json
    
    @staticmethod
    def decode(stream):
        stream = io.BytesIO(b'{"title":"News 666","content":"\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82: \xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8\xd1\x80\xd1\x83\xd0\xb5\xd0\xbc \xd1\x80\xd1\x83\xd1\x87\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x81\xd0\xb5\xd1\x80\xd0\xb8\xd0\xb0\xd0\xbb\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80"}')
        data = JSONParser().parse(stream)
        serializer = NewsModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
    
    @staticmethod
    def decode_from_post(stream):
        serializer = NewsModelSerializer(data=stream)
        serializer.is_valid()
        return serializer.validated_data



def encode():
    # Создаем Объект Модели NewsModel
    model = NewsModel("News 666", "Контент: Тестируем ручной сериализатор")
    # Объект сериализации - Обрабатываем Объект, model, нашим ручным сериализатором NewsModelSerializer
    model_sr = NewsModelSerializer(model)
    # Вывод результата при помощи атрибута .data - это Сериализованые данные
    print(model_sr.data, type(model_sr.data), sep='\n')
    # Создаем JSON строку
    json = JSONRenderer().render(model_sr.data)
    print(json.decode('utf-8'))
    print(json)
    return json


def decode():
    # Принимаем строку JSON
    stream = io.BytesIO(b'{"title":"News 666","content":"\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82: \xd0\xa2\xd0\xb5\xd1\x81\xd1\x82\xd0\xb8\xd1\x80\xd1\x83\xd0\xb5\xd0\xbc \xd1\x80\xd1\x83\xd1\x87\xd0\xbd\xd0\xbe\xd0\xb9 \xd1\x81\xd0\xb5\xd1\x80\xd0\xb8\xd0\xb0\xd0\xbb\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80"}')
    print(stream)
    # Преобразуем в Словарь
    data = JSONParser().parse(stream)
    print(data)
    # Получаем объект сериализации - Приводим данные в нужный нам формат сериализатором (передаем в именованный аргумент data)
    serializer = NewsModelSerializer(data=data)
    print(serializer)
    # Проверка корректности принятых данных
    serializer.is_valid()
    # Результат декодирования принятой - stream
    print(serializer.validated_data,type(serializer.validated_data))







class NewsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    class Meta:
        model = News
        #fields = ('title', 'content','category')
        fields = '__all__'