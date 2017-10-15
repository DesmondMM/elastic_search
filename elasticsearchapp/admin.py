from django.contrib import admin

from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'posted_date', 'title')


admin.site.register(BlogPost, BlogPostAdmin)
