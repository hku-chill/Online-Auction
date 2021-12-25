from django.contrib import admin
from .models import category, auction, bid, comment

class categoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'name', 'auction_count')
    list_display_links = ('pk', 'slug')
    search_fields = ('pk', 'name', 'slug')

# class auctionAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'slug', 'name')

class auctionAdmin(admin.ModelAdmin):
    list_display = ('pk','item_title', 'slug')


class bidAdmin(admin.ModelAdmin):
    list_display = ('pk', 'auction', 'user', 'bid_amount', 'bid_date', 'is_bid_highest')


class commentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'auction', 'user', 'created')


# admin.site.register(auction, auctionAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(auction, auctionAdmin)
admin.site.register(bid, bidAdmin)
admin.site.register(comment, commentAdmin)
# Register your models here.
