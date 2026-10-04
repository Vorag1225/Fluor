from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user','description','icon']
    list_filter = []
    search_fields = ['user__username','user__first_name']