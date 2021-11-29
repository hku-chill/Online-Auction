from django.shortcuts import render, HttpResponse

# Create your views here.

def user_register(request):
    if request.user.is_authenticated:
        return HttpResponse("You are already logged in.")
        
    return render(request, 'user/_index.html', {'name' : request})

def user_login(request):
    return HttpResponse('login')