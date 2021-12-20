from django.urls import path

from .views import *

urlpatterns = [
    path('category/<str:slug>/', get_category, name="category_item_url"),
    path('category/', get_category_list, name="category_index_url"),

    path('auction/', get_auction_list, name="auction_index_url"),
    path('auction/<str:slug>/', get_auction, name="auction_item_url"),

    path('auction/bid/<str:slug>/', add_bid_to_auction, name="auction_bid_url"),

    path('auction/comment/<str:slug>/', add_comment, name="add_comment_url"),
]
