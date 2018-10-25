from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404


def create(request):
    form = UserCreationForm()
    return render(request, 'accounts/new.html', {'form': form})
