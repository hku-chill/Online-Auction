from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def base_index(request):
    return render(request, 'base/_index.html')