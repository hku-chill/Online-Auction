from django.contrib import admin
from .models import category, auction

class categoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'name', 'auction_count')
    list_display_links = ('pk', 'slug')
    search_fields = ('pk', 'name', 'slug')

class auctionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'name')

admin.site.register(auction, auctionAdmin)
admin.site.register(category, categoryAdmin)
# Register your models here.
