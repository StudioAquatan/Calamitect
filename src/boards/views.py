from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return render(request, 'boards/index.html')


def create(request):
    form = UserCreationForm()
    return render(request, 'boards/new.html', {'form': form})
