from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator



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
    comments = post.comments.filter(active=True)
    awaiting_comments = post.comments.filter(active=False, author=request.user)
    new_comment = None

    # Increment view count
    post.number_of_views += 1
    post.save()

    if request.method == 'POST':
        if 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment_form = CommentForm(request.POST, instance=comment)
            if comment_form.is_valid():
                comment_form.save()
                messages.add_message(request, messages.SUCCESS, 'Your comment has been updated.')
            return redirect('post_detail', slug=slug)
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id, author=request.user)
            comment.delete()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been deleted.')
            return redirect('post_detail', slug=slug)
        else:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                if request.user.is_authenticated:
                    new_comment.author = request.user
                    new_comment.active = False  # Awaiting approval
                    new_comment.save()
                    messages.add_message(request, messages.INFO, 'Your comment is awaiting approval.')
                return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'awaiting_comments': awaiting_comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'number_of_likes': post.number_of_likes,
        'number_of_saves': post.number_of_saves,
        'number_of_shares': post.number_of_shares,
    })

def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    post = comment.post
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been updated.')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm(instance=comment)
    
    return render(request, 'edit_comment.html', {
        'comment_form': comment_form,
        'post': post
    })

def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id, author=request.user)
    post = comment.post
    if request.method == 'POST':
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Your comment has been deleted.')
        return redirect('post_detail', slug=post.slug)
    
    return render(request, 'delete_comment.html', {'comment': comment, 'post': post})