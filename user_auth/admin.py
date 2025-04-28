from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_verified', 'is_editor', 'joined')
    ordering = ('-joined',)

    fieldsets = (
        (None, {'fields':('username','password')}),
        ('personal_info', {'fields':('first_name','last_name', 'email', 'is_verified', 'is_editor')}),
        ('Permissions', {'fields':('is_active','is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
admin.site.register(CustomUser, CustomUserAdmin)
