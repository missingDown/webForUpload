from django.urls import path
from . import views

urlpatterns = [
    path('api/sinoyd-dynamic/dynamic/interface/uploadphotosformdata', views.index, name='index'),
    path('api/sinoyd-dynamic/dynamic/interface/uploadphotosbase64', views.body, name='body'),
    path('getpicture/testface.png', views.picture, name='picture'),
    path('ISAPI/Intelligent/FDLib/FDSetUp', views.puttest, name='picture'),
]