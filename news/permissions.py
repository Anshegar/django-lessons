from rest_framework import permissions 

# Просмотр всеми, Изменение только Админом
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):        # ПЕРЕОПРЕДЕЛЯЕМ Метод РД класса BasePermission
        if request.method in permissions.SAFE_METHODS:      # Проверяем, безопасный ли запрос(GET,HEAD,OPTIONS)
            return True                                     # Предоставляем допуск
        return bool(request.user and request.user.is_staff) # Если Админ то ему разрешены небезопасные Запросы
    
# Просмотр всеми, Изменение только Создателем записи
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj): # Принимает атрибуты объекта
        if request.method in permissions.SAFE_METHODS:      # Проверяем, безопасный ли запрос(GET,HEAD,OPTIONS)
            return True
        return obj.user == request.user                    # Если данные из строки НАШЕЙ Модели (строка FK user) 
        # --- совпал с данными из ЗАПРОСА по имени атрибута user, то полный доступ  

# --- Что бы узнать как давать допуск того или иного уровня просто смотрим Definitions (к примеру IsAdminUser)