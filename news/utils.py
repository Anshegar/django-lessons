# Создание миксина
#class MyMixin:
class MyMixin(object):  # Может ничего не принимать, а может принимать, это не критично
    mixin_prop =''      # Свойства для перегрузки\переактивации\перезаписи

    def get_prop(self):
        return self.mixin_prop.upper()
# Теперь его можно наследовать в наших классах в проекта class SomeName(ListView, MyMixin):
    
    def get_upper(self,s):
        if isinstance(s, str):          # Если строка то обрабатываем напрямую
            return s.upper()
        else:                           # Если нет, предполагаем что это Объект и обращаемся к его атрибуту
            return s.title.upper()