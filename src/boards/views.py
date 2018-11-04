from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import django_filters
from rest_framework import viewsets, filters
from src.accounts.models import User
from .models import Article, Good, Favorite, Comment
from .serializer import GoodSerializer, FavoriteSerializer, CommentSerializer


def index(request):
    print(request.user.is_authenticated)

    try:
        articles = Article.objects.all()
    except Article.DoesNotExist:
        empty = "まだ記事が投稿されていません。"
        return render(request, 'boards/index.html', {'empty': empty})

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/index.html', {'articles': articles, 'user_id': user_id})

    return render(request, 'boards/index.html', {'articles': articles})


def categoryTop(request):
    category_type = request.GET['category_type']

    try:
        articles = Article.objects.filter(category_type=category_type)
        print(articles)
    except Article.DoesNotExist:
        empty = "まだ記事が投稿されていません。"
        print("ssffd")
        return render(request, 'boards/category_top.html', {'empty': empty})

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/category_top.html',
                      {'articles': articles, 'user_id': user_id, 'category_type': category_type})

    return render(request, 'boards/category_top.html', {'articles': articles, 'category_type': category_type})


def create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST['title']
            description = request.POST['description']
            category_type = request.POST['category_type']
            draft_flag = request.POST['draft_flag']
            Article.objects.create(
                title=title,
                description=description,
                category_type=category_type,
                draft_flag=draft_flag,
                user=request.user
            )

            return redirect('boards:index')

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/index.html', {'user_id': user_id})

    return render(request, 'boards/new.html')


def articleDetail(request, article_id):
    articles = Article.objects.get(id=article_id)
    print(articles.title)
    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/article_detail.html', {'articles': articles, 'user_id': user_id})

    return render(request, 'boards/article_detail.html', {'articles': articles})


class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# 以下のアクションは仮配置

def userPage(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/userpage.html', {'user_id': user_id, 'user': user})


def newPost(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/new_post.html', {'user_id': user_id, 'user': user})


def postAll(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

        try:
            articles = Article.objects.filter(user=user)
        except Article.DoesNotExist:
            empty = "まだ記事が投稿されていません。"
            return render(request, 'accounts/post_all.html', {'user_id': user_id, 'empty': empty})

    return render(request, 'accounts/post_all.html', {'user_id': user_id, 'user': user, 'articles': articles})


def good(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/good.html', {'user_id': user_id, 'user': user})


def favorite(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/favorite.html', {'user_id': user_id, 'user': user})
