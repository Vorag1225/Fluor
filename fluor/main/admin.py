from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','description','icon']
    list_filter = []
    search_fields = ['user__username','user__first_name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'text', 'author__username', 'author__first_name']