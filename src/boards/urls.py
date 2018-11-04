from django.urls import path
from rest_framework import routers

from . import views
from .views import GoodViewSet, FavoriteViewSet, CommentViewSet

app_name = 'boards'

router = routers.DefaultRouter()
router.register(r'goods', GoodViewSet)
router.register(r'favorite', FavoriteViewSet)
router.register(r'comment', CommentViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('boards/new/', views.create, name='create'),
    path('boards/category-top', views.categoryTop, name='categoryTop')
]