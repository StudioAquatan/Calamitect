from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boards/new/', views.create, name='create'),
]