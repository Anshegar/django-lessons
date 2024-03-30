from django.urls import path
from .views import * 
#from .apiviews import * 
from django.views.decorators.cache import cache_page


urlpatterns = [
    #path('api/v1/newsapilist',NewsAPIList.as_view(), name = "NewsAPIList"),
    #path('api/v1/newsapilist/<int:id>/',NewsAPIList.as_view(), name = "NewsAPIList"),
    #path('api/v1/newsmodellistdb/<int:id>/',NewsModelAPIView_DB.as_view(), name = "NewsModelAPIViewDB"),
    #path('api/v1/newsmodellistdb',NewsModelAPIView_DB.as_view(), name = "NewsModelAPIViewDB"),
    #path('api/v1/newslist',NewsAPIView.as_view(), name = "NewsAPIView"),
    #path('api/v1/newslist/<int:id>/',NewsAPIView.as_view(), name = "NewsAPIView"),
    #path('api/v1/newsmodellist',NewsModelAPIView.as_view(), name = "NewsModelAPIView"),
    #path('api/v1/newslistnoser',NewsAPIViewNoSerializer.as_view(), name = "NewsAPIViewNoSerializer"),
    path('register/',register, name = "register"),
    path('login/',user_login, name = "login"),
    path('logout/',user_logout, name = "logout"),
    #path('', index, name = "home"),
    path('', HomeNews.as_view(), name = "home"),
    #path('',cache_page(60)(HomeNews.as_view()), name = "home"),
    path('test/', test, name = "test"),
    path('contact/', contact, name = "contact"),
    #path('category/<int:category_id>',get_category, name = "category"),
    path('category/<int:category_id>/',NewsByCategory.as_view(extra_context = {"title":"Категории"}), name = "category"),
    #path('news/<int:news_id>',view_news, name = "view_news"),
    #path('news/<int:news_id>',ViewNews.as_view(), name = "view_news"),
    path('news/<int:pk>/',ViewNews.as_view(), name = "view_news"),
    #path('news/add-news',add_news, name = "add_news"),
    path('news/add-news/',CreateNews.as_view(), name = "add_news"),

]