from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
# from . import Article


def index(request):
    return render(request, 'boards/index.html')


def create(request):

    if request.method == 'POST':
        title = request.POST['title']
        message = request.POST['message']

        user = User.objects.first()

        # topic = Article.objects.create(
        #     title=title,
        #     board=,
        #     starter=user
        # )

        return redirect('index')

    return render(request, 'boards/new.html')