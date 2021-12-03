from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'user_is_active', 'is_email_verified', 'is_phone_verified')
    list_filter = ('is_email_verified', 'is_phone_verified')
    search_fields = ('is_email_verified', 'is_phone_verified')
    ordering = ('pk', 'is_email_verified', 'is_phone_verified')


    def user_is_active(self, x):
        return x.user.is_active





    
    user_is_active.user_is_active = 'is_active'

admin.site.register(Profile, ProfileAdmin)