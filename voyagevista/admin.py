from django.contrib import admin
from .models import Post, Category
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the Post model.
    """
    prepopulated_fields = {'slug': ('title',)}

    """
Specifies the fields to be displayed in the admin interface, the fields used for search, 
the field filters, the fields to be prepopulated, and the configuration for the rich-text editor.
"""

    list_filter = ('status', 'created_on', 'approved', 'author', 'updated_on', 'category')
    summernote_field = ('content')
    list_display = ('status', 'created_on', 'approved', 'slug', 'title', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)



# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    prepopulated_fields = {'slug': ('name',)}