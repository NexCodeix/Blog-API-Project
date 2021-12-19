from django.contrib import admin
from .models import Blog, Tag, BlogImage

class BlogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "content")


admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(BlogImage)

