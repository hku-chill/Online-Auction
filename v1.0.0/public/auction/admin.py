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

# admin.site.register(auction, auctionAdmin)
admin.site.register(category, categoryAdmin)
admin.site.register(auction, auctionAdmin)
admin.site.register(bid)
admin.site.register(comment)
# Register your models here.
