from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
import django_filters
from rest_framework import viewsets, filters
from django.views import View
from accounts.models import User
from .models import Article, Good, Favorite, Comment, Tag
from .forms import CreateArticleForm
from .serializer import GoodSerializer, FavoriteSerializer, CommentSerializer
import time
import timeout_decorator
from accounts.forms import LoginUserForm

def index(request):
    # 緊急地震情報
    quake_info, display = get_quake_info()
    if "emergency" in request.GET:
        display = True
    else:
        display = False

    try:
        articles = Article.objects.all()
        articles = articles.order_by("created_at").reverse()
    except Article.DoesNotExist:
        articles = None

    if request.user.is_authenticated:
        user = request.user
        return render(request, 'boards/index.html', {'articles': articles, 'user': user,'user_id': user.id,'quake_info':quake_info, 'display':display})

    return render(request, 'boards/index.html', {'articles': articles, 'quake_info':quake_info, 'display':display})


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
        search_words = None

    # ソートタイプ取得
    if 'sort_type' in request.GET:
        sort_type = request.GET['sort_type']
    else:
        sort_type = None

    if search_words:
        # 検索で取得
        articles = Article.objects.filter(Q(description__icontains=search_words) | Q(title__icontains=search_words))
    else:
        articles = None

    if sort_type == '1':
        # createdが新しい順(降順)
        articles = articles.order_by('created_at').reverse()
    elif sort_type == '2':
        # createdが古い順(昇順)
        articles = articles.order_by('created_at')

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        return render(request, 'boards/search.html',
                      {'articles': articles, 'user_id': user_id, 'search_words': search_words, 'sort_type': sort_type})

    return render(request, 'boards/search.html',
                  {'articles': articles, 'search_words': search_words, 'sort_type': sort_type})


class CreateArticleView(View):
    def get(self, request, *args, **kwargs):
        get_object_or_404(User, pk=request.user.id)
        if request.user.is_authenticated:
            context = {
                'user_id': request.user.id,
                'user': request.user,  # TODO user渡せばuser_id渡さなくてもいい気がする
                'form': CreateArticleForm,
            }
            return render(request, 'accounts/new_post.html', context)
        else:
            return  # TODO ここに404ページへのredirectを配置

    def post(self, request):
        form = CreateArticleForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            context = {
                'user_id': request.user.id,
                'user': request.user,  # TODO user渡せばuser_id渡さなくてもいい気がする
                'form': form,
            }
            return render(request, 'accounts/new_post.html', context)
        article = form.save(commit=False)
        article.category_type = request.POST['category_type']
        article.draft_flag = request.POST['draft_flag']
        article.user = request.user
        article.save()
        return redirect('boards:index')


create_article = CreateArticleView.as_view()


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

    enter_login_form = False
    try:
        is_good = Good.objects.filter(user=request.user, article=article).count()
    except:
        is_good = 0
        enter_login_form = True




    done_good_flag = 0
    if is_good != 0:
        done_good_flag = 1

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id
        if request.method == 'POST':
            return redirect('boards:article_detail',article_id=article_id)

        return render(request, 'boards/article_detail.html',
                      {'articles': articles, 'article_id': article_id, 'good_sum': good_sum, 'user_id': user_id,
                       'comments': copy_comments, 'comments_sum': comments_sum, 'tags':tags,'done_good_flag':done_good_flag, 'enter_login_form':enter_login_form, 'form': LoginUserForm})

    return render(request, 'boards/article_detail.html',
                  {'articles': articles, 'article_id': article_id, 'good_sum': good_sum, 'comments': copy_comments,
                   'comments_sum': comments_sum,'tags':tags,'done_good_flag':done_good_flag, 'enter_login_form':enter_login_form, 'form': LoginUserForm})


def good(request):
    article_id = int(request.POST['article_id'])
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


def favorite(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'accounts/favorite.html', {'user_id': user_id, 'user': user})



#  地震速報の取得

import urllib.request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError

def get_quake_info():
    # 緊急速報の取得
    try:
        html = urllib.request.urlopen("http://www.jma.go.jp/jp/quake/quake_sindo_index.html",timeout=2)
    except (HTTPError, URLError) as error:
        # タイムアウト処理
        return 0, 0
    soup = BeautifulSoup(html, "lxml")
    infotable = soup.find_all("div", attrs={"id": "info", "class": "infotable"})

    # 緊急速報の中での最新詳細情報のURL取得
    base_link = "http://www.jma.go.jp/jp/quake"
    add_link = infotable[0].a.get("href")
    link = base_link + add_link.lstrip(".")

    # 最新情報取得
    html_up_to_date = urllib.request.urlopen(link)
    soup_up_to_date = BeautifulSoup(html_up_to_date, "lxml")
    infotable_up_to_date = soup_up_to_date.find_all("table", attrs={"id": "infobox", "class": "textframe"})
    get_text = infotable_up_to_date[0].text

    # 余分な文字消去
    get_text = get_text.replace("震度速報","")
    #　配列化
    get_text_array = get_text.split("\n")

    info = []
    for i in range(len(get_text_array)):
        get_text_array[i] = get_text_array[i].strip()

        if "気象庁発表" in get_text_array[i]:
            string_array = get_text_array[i].split("気象庁発表")
            for j in range(len(string_array)):
                if j == 0:
                    # ”気象庁発表”が消えたので追加する
                    string_array[j] = string_array[j] + "気象庁発表"
                info.append(string_array[j])

        elif "震度" in get_text_array[i]:
            string_array = get_text_array[i].split("震度")
            for k in range(len(string_array)):
                if k > 0:
                    # ”震度”が消えたので追加する
                    string_array[k] = "震度" + string_array[k]
                info.append(string_array[k])
        else:
            info.append(get_text_array[i])

    # 空白のリスト要素を除去
    info = list(filter(lambda x: x != "", info))

    display_on_off = False
    for _info in info:
        if "震度３" in _info:
            display_on_off =True

    return info, display_on_off

