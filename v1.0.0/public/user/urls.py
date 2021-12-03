from django.urls import path
from django.contrib import admin
from .views import *


urlpatterns = [


    path('register/', register_user, name="user_register_url"),
    path('login/', login_user, name="user_login_url"),
    path('logout/', user_logout, name="user_logout_url"),
    # path('activate/<uidb64>/', activate_mail, name="activate_url"),


    path(
        'activate/<str:uid64>/',
        mail_activate,
        name = "user_mail_activate_url"
    ),
]
