from django.urls import path
from .views import *

urlpatterns = [
    path('category/<str:slug>/', get_category, name="category_item_url"),
    path('category/', get_category_list, name="category_index_url"),
    path('auction/', get_auction_list, name="auction_index_url"),
]