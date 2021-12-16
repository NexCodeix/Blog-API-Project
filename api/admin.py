from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "last_updated"]


admin.site.register(Blog, BlogAdmin)
