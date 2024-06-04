from django.contrib import admin
from .models import Post, Category, Comment
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
Specifies the fields to be displayed in the admin interface, the fields used for search, 
the field filters, the fields to be prepopulated, and the configuration for the rich-text editor.
"""
    list_filter = ('status', 'created_on', 'approved', 'author', 'updated_on', 'category')
    list_display = ('status', 'created_on', 'approved', 'slug', 'title', 'author')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    summernote_fields = ('content',)




# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Configure the admin list view for the Comment model to show the post, author, and approval status.
    """
    list_display = ('post', 'created_on', 'author', 'approved')
    list_filter = ('author', 'created_on', 'approved')
    search_fields = ('email', 'author', 'title')