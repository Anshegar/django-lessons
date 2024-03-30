from django.urls import path, include
from .apiviews import * 
from .routers import *
from django.views.decorators.cache import cache_page
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'newsapiviewsetrouter', NewsViewSet, basename='news')







urlpatterns = [
    path('api/v1/', include(router.urls)),
    # path('api/v1/newsapiviewset/', NewsViewSet.as_view({'get': 'list'}), name="NewsAPIViewSet"),
    # path('api/v1/newsapiviewset/<int:pk>/',NewsViewSet.as_view({'put': 'update'}), name = "NewsAPIViewSet"),

    path('api/v1/newsjwtapiupdate/<int:pk>/',NewsJWTTokenAPIUpdate.as_view(), name = "NewsJWTTokenAPIUpdate"),
    path('api/v1/newsapicrud/<int:pk>/',NewsAPIFullCRUD.as_view(), name = "NewsAPICRUD"),
    path('api/v1/newsapireterdelete/<int:pk>/',NewsAPIRetrDestroy.as_view(), name = "NewsAPIRetrDestroy"),
    path('api/v1/newsapiupdate/<int:pk>/',NewsAPIUpdate.as_view(), name = "NewsAPIUpdate"),
    path('api/v1/newsapilist/',NewsAPIList.as_view(), name = "NewsAPIList"),
    path('api/v1/newsmodellistdb/<int:id>/',NewsModelAPIView_DB.as_view(), name = "NewsModelAPIViewDB"),
    path('api/v1/newsmodellistdb/',NewsModelAPIView_DB.as_view(), name = "NewsModelAPIViewDB"),
    path('api/v1/newslist/',NewsAPIView.as_view(), name = "NewsAPIView"),
    path('api/v1/newslist/<int:id>/',NewsAPIView.as_view(), name = "NewsAPIView"),
    path('api/v1/newsmodellist/',NewsModelAPIView.as_view(), name = "NewsModelAPIView"),
    path('api/v1/newslistnoser/',NewsAPIViewNoSerializer.as_view(), name = "NewsAPIViewNoSerializer"),

    path('api/v1/drf-auth/', include('rest_framework.urls')),

]