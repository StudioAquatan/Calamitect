from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import django_filters
from rest_framework import viewsets, filters
from accounts.models import User
from .models import Article, Good, Favorite, Comment, Tag
from .serializer import GoodSerializer, FavoriteSerializer, CommentSerializer


def index(request):
    print(request.user.is_authenticated)

    try:
        articles = Article.objects.all()
        articles.order_by("created_at").reverse()
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

    if 'sort_type' in request.GET:
        sort_type = request.GET['sort_type']
    else:
        sort_type = 0

    if 'search_key' in request.POST:
        search_key = request.POST['search_key']
    else:
        search_key = 0

    try:
        # 先に全件取得
        articles = Article.objects.filter(category_type=category_type)
        print(articles)
    except Article.DoesNotExist:
        empty = "まだ記事が投稿されていません。"
        return render(request, 'boards/category_top.html', {'empty': empty})

    if sort_type == '1':
        # createdが新しい順(降順)
        articles = articles.order_by('created_at').reverse()
    if sort_type == '2':
        # createdが古い順(昇順)
        articles = articles.order_by('created_at')

    if search_key:
        # 検索時
        articles = Article.objects.filter(Q(description__icontains=search_key) | Q(title__icontains=search_key) ,category_type=category_type)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/category_top.html',
                      {'articles': articles, 'user_id': user_id, 'category_type': category_type,
                       'sort_type': sort_type})

    return render(request, 'boards/category_top.html',
                  {'articles': articles, 'category_type': category_type, 'sort_type': sort_type})


def search(request):
    # 検索ワード取得
    if 'search_words' in request.POST:
        search_words = request.POST['search_words']
    elif 'search_words' in request.GET:
        search_words = request.GET['search_words']
    else:
        search_words = 0

    # ソートタイプ取得
    if 'sort_type' in request.GET:
        sort_type = request.GET['sort_type']
    else:
        sort_type = 0

    if search_words:
        # 検索で取得
        articles = Article.objects.filter(Q(description__icontains=search_words) | Q(title__icontains=search_words))
    else:
        articles = None

    if sort_type == '1':
        # createdが新しい順(降順)
        articles = articles.order_by('created_at').reverse()
    if sort_type == '2':
        # createdが古い順(昇順)
        articles = articles.order_by('created_at')

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/search.html',
                      {'articles': articles, 'user_id': user_id, 'search_words': search_words, 'sort_type': sort_type})

    return render(request, 'boards/search.html',
                  {'articles': articles, 'search_words': search_words, 'sort_type': sort_type})


def create(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST['title']
            description = request.POST['description']
            category_type = request.POST['category_type']
            draft_flag = request.POST['draft_flag']
            article = Article.objects.create(
                title=title,
                description=description,
                category_type=category_type,
                draft_flag=draft_flag,
                user=request.user
            )

            tag_name = request.POST['tag']
            Tag.objects.create(
                name=tag_name,
                article=article
            )

            return redirect('boards:index')

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/index.html', {'user_id': user_id})

    return render(request, 'boards/new.html')


def articleDetail(request, article_id):
    articles = Article.objects.get(id=article_id)
    article = Article.objects.get(id=article_id)
    tags = Tag.objects.filter(article=articles)

    # comment作成時
    if request.method == 'POST':
        text = request.POST['text']
        user = request.user
        Comment.objects.create(
            text=text,
            user=user,
            article=article,
        )
    comments = Comment.objects.filter(article=articles)

    import copy
    copy_comments = copy.deepcopy(comments)
    for copy in copy_comments:
        _user = User.objects.get(id=copy.user_id)
        copy.username = _user.username

    comments_sum = comments.count()
    good_sum = Good.objects.filter(article=articles).count()

    is_good = Good.objects.filter(user=request.user, article=article).count()
    double_flag = 0
    if is_good != 0:
        double_flag = 1


    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        if request.method == 'POST':
            return redirect('boards:article_detail',article_id=article_id)

        return render(request, 'boards/article_detail.html',
                      {'articles': articles, 'article_id': article_id, 'good_sum': good_sum, 'user_id': user_id,
                       'comments': copy_comments, 'comments_sum': comments_sum, 'tags':tags,'double_flag':double_flag})

    return render(request, 'boards/article_detail.html',
                  {'articles': articles, 'article_id': article_id, 'good_sum': good_sum, 'comments': copy_comments,
                   'comments_sum': comments_sum,'tags':tags,'double_flag':double_flag})


def good(request, article_id):
    article = Article.objects.get(id=article_id)
    is_good = Good.objects.filter(user=request.user, article=article).count()

    if is_good != 0:
        good = Good.objects.get(user=request.user, article=article)
        good.delete()
        return redirect('boards:article_detail', article_id=article_id)

    Good.objects.create(
        user=request.user,
        article=article
    )
    return redirect('boards:article_detail', article_id=article_id)


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

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        category_type = request.POST['category_type']
        draft_flag = request.POST['draft_flag']


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

            for article in articles:
                sum = Good.objects.filter(article=article).count()
                article.good_sum = sum

        except Article.DoesNotExist:
            empty = "まだ記事が投稿されていません。"
            return render(request, 'accounts/post_all.html', {'user_id': user_id, 'empty': empty})

    return render(request, 'accounts/post_all.html', {'user_id': user_id, 'user': user, 'articles': articles})


def postEdit(request, user_id, article_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

        articles = Article.objects.get(id=article_id)

        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            category_type = request.POST['category_type']
            draft_flag = request.POST['draft_flag']

            articles.title = title
            articles.description = description
            articles.category_type =category_type
            articles.draft_flag =draft_flag
            articles.save()

            return redirect('boards:post_edit', article_id=article_id, user_id=user_id )
    return render(request, 'accounts/post_edit.html', {'user_id': user_id, 'user': user, 'articles': articles})


def myGood(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

        goods = Good.objects.filter(user=user)
        for good in goods:
            sum = Good.objects.filter(article=good.article).count()
            good.article.good_sum = sum

        return render(request, 'accounts/good.html', {'user_id': user_id, 'user': user, 'goods': goods})

    return render(request, 'accounts/good.html', {'user_id': user_id, 'user': user})


def myFavorite(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/favorite.html', {'user_id': user_id, 'user': user})
