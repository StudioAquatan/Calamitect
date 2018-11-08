from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import RegisterUserForm


class RegisterView(View):
    def get(self, request):
        context = {
            'form': RegisterUserForm
        }
        return render(request, 'accounts/new.html', context)

    def post(self, request):
        form = RegisterUserForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            return render(request, 'accounts/new.html',
                          {'form': form})
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('boards:index')




register = RegisterView.as_view()


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
            return render(request, 'accounts/login.html', {'error': error})

        # user = authenticate(request, username=username, password=password)

    return render(request, 'accounts/login.html')


def logOut(request):
    logout(request)

    return render(request, 'boards/index.html')
