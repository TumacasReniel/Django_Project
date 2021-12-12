from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


from .models import User


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','email','is_superuser')

admin.site.register(User, UserAdmin)
