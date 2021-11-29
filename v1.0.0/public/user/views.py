from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

# Create your views here.

def user_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'user/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'user/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')