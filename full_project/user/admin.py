from django.contrib import admin
from .models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'password', 'created_at', 'updated_at')
    search_fields = ('first_name', 'last_name', 'email', 'password', 'created_at', 'updated_at')
    list_filter = ('first_name', 'last_name', 'email', 'password', 'created_at', 'updated_at')

admin.site.register(User, UserAdmin)
