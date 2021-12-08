from django.urls import path
from .views import *


urlpatterns = [


    path('register/', register_user, name="user_register_url"),
    path('login/', login_user, name="user_login_url"),
    path('logout/', user_logout, name="user_logout_url"),

    path('profile/', user_profile, name="user_self_profile_url"),
    path('profile/<int:userid>', user_profile_id, name="user_profile_url"),

    path('profile/tc/', user_tc_validate_view, name="user_tc_url"),
    path('profile/tc/validate/', user_tc_validate_end, name="user_tc_validate_url"),
    # path('activate/<uidb64>/', activate_mail, name="activate_url"),


    path(
        'activate/<str:uid64>/',
        mail_activate,
        name = "user_mail_activate_url"
    ),
]
