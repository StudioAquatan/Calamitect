from django.contrib.auth import authenticate, login, logout
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from src.boards.models import Article, Tag

# auth user model のカスタムモデルを利用
from django.contrib.auth import get_user_model
User = get_user_model()



class UserCreationForm(BaseUserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    class Meta:
        model = User
        fields = fields = ("username", "email", "password1", "password2")




def create(request):
    form = UserCreationForm(request.POST)
    error_flag = 0
    if request.method == 'POST':

        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password1']
            user = User.objects.create(
                username=username,
                email=email,
                password=password
            )
            # form.save()

            login(request, user)
            return redirect('boards:index')
        else:
            error_flag = 1
            return render(request, 'accounts/new.html', {'form': form, 'error_flag':error_flag})


    return render(request, 'accounts/new.html', {'form': form, 'error_flag':error_flag})



def logIn(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(
                username=username,
                password=password,
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('boards:index')
        except User.DoesNotExist:
            error = "名前かパスワードに誤りがあります。"
            return render(request, 'accounts/login.html',{ 'error': error})

        # user = authenticate(request, username=username, password=password)

    return render(request, 'accounts/login.html')


def logOut(request):
    logout(request)

    return render(request, 'boards/index.html')













