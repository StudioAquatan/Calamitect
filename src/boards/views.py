from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article

def index(request):
    print(request.user.is_authenticated)
    return render(request, 'boards/index.html')

def categoryTop(request):
    category_type = request.GET['category_type']

    try:
        articles = Article.objects.filter(category_type=category_type)
        print(articles)
    except Article.DoesNotExist:
        empty = "まだ記事が投稿されていません。"
        print("ssffd")
        return render(request, 'boards/category_top.html', {'empty': empty})

    return render(request, 'boards/category_top.html', {'articles': articles})

def create(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            title = request.POST['title']
            description = request.POST['description']
            category_type = request.POST['category_type']


            Article.objects.create(
                title=title,
                description=description,
                category_type=category_type,
                user=request.user
            )

            return render(request, 'boards/index.html')

    return render(request, 'boards/new.html')