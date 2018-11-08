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
    path('boards/new/', views.create_article, name='create'),
    path('boards/category-top', views.categoryTop, name='categoryTop'),
    path('boards/search', views.search, name='search'),
    path('boards/article-detail/<int:article_id>/', views.articleDetail, name='article_detail'),
    path('boards/good/', views.good, name='good'),

    path('<int:user_id>/', views.userPage, name='userpage'),
    path('<int:user_id>/new_post/', views.create_article, name='newpost'),
    path('<int:user_id>/post_all/', views.postAll, name='postall'),
    path('<int:user_id>/post_edit/<int:article_id>/', views.postEdit, name='post_edit'),
    path('<int:user_id>/good/', views.myGood, name='mygood'),
    path('<int:user_id>/favorite/', views.favorite, name='favorite'),
]
