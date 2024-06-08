from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from .forms import CommentForm


def category_view(request, category_slug=None):
    """
    View for displaying posts filtered by category.
    """
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(status=1).order_by('-created_on')

    if category_slug:
        category = Category.objects.get(slug=category_slug)
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    }

    return render(request, 'index.html', context)


def post_detail(request, slug):
    """
    View for displaying the details of a single post.
    """
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, active=True)
    
    # Increment view count
    post.number_of_views += 1
    post.save()

    # Handle new comment submission
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.name = request.user.username  # Set the comment name to the user's username
                new_comment.email = request.user.email  # Set the comment email to the user's email
                new_comment.active = False  # Set the comment to inactive (awaiting approval)
                new_comment.save()
                messages.add_message(request, messages.INFO, 'Your comment is awaiting approval.')
            else:
                new_comment.active = True  # Directly set to active if not logged in
                new_comment.save()
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post_detail.html', context)