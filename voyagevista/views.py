from django.shortcuts import render, get_list_or_404
from django.views import generic
from .models import Post, Category


class PostList(generic.ListView):
    """
    View for displaying a list of published posts.
    """
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 4


def category_view(request, category_slug):
    """
    View for displaying posts in a specific category.
    """
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status=1).order_by('-created_on')
    return render(request, 'category.html', {'category': category, 'posts': posts})