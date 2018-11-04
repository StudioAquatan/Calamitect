from django.contrib.auth import authenticate, login, logout
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

    class Meta:
        model = User
        fields = 'username',




def create(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create(
            username=username,
            email = email,
            password = password
        )

        form = UserCreationForm(request.POST)
        login(request, user)
        if form.is_valid():
            print("nvoenbejhu")
            user = form.save()

            return redirect('boards:index')


    return render(request, 'accounts/new.html')



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

    if request.user.is_authenticated:
        user = request.user
        user_id = user.id

    return render(request, 'boards/index.html',{'user_id':user_id})













