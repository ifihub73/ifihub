from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import EditorRequest


# Register your models here.

class EditorRequestAdmin(ModelAdmin):
    list_display =('user', 'approved', 'date')
    ordering = ('-date',)

admin.site.register(EditorRequest, EditorRequestAdmin)
