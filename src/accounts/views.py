from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import RegisterUserForm, LoginUserForm


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
            return render(request, 'accounts/new.html', {'form': form})
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        auth_login(request, user)
        return redirect('boards:index')


class LoginView(View):
    def get(self, request):
        context = {
            'form': LoginUserForm
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = LoginUserForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            return render(request, 'accounts/login.html', {'form': form})
        user = form.get_user()
        auth_login(request, user)
        return redirect('boards:index')


class LogoutView(View):
    def get(self, request):
        auth_logout(request)
        return redirect('boards:index')


register = RegisterView.as_view()
login = LoginView.as_view()
logout = LogoutView.as_view()
