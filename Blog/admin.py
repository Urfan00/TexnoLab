from django.contrib import admin
from .models import Blog, BlogCategory



class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    search_fields = ['name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'photo', 'date', 'blog_category', 'status', 'created_at', 'updated_at']
    list_filter = ['status']
    list_display_links = ['id', 'title', 'slug']
    search_fields = ['title', 'blog_category__name']


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)

