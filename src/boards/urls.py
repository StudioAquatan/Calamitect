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
    path('boards/category-top', views.categoryTop, name='categoryTop'),

    path('<int:user_id>/', views.userPage, name='userpage'),
    path('new_post/<int:user_id>/', views.newPost, name='newpost'),
    path('post_all/<int:user_id>/', views.postAll, name='postall'),
    path('good/<int:user_id>/', views.good, name='good'),
    path('favorite/<int:user_id>/', views.favorite, name='favorite'),
]