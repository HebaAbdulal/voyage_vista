from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment
from django.core.paginator import Paginator
from .forms import CommentForm
from django.http import JsonResponse
from django.contrib import messages


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
    awaiting_comments = Comment.objects.filter(post=post, active=False, author=request.user) if request.user.is_authenticated else []
    new_comment = None

    # Increment view count
    post.number_of_views += 1
    post.save()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.author = request.user
                new_comment.active = False  # Awaiting approval
                new_comment.save()
                messages.add_message(request, messages.INFO, 'Your comment is awaiting approval.')
            else:
                new_comment.active = True
                new_comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'author': new_comment.author.username,
                    'created_on': new_comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                    'body': new_comment.body,
                })
            else:
                return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    
    if comments:
        context['comment_id'] = comments.first().id  # Assigning comment ID if available
    
    return render(request, 'post_detail.html', context)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment_form.save()
            return JsonResponse({'success': True})
    else:
        comment_form = CommentForm(instance=comment)

    context = {
        'comment': comment,
        'comment_form': comment_form,
    }
    return render(request, 'edit_comment.html', context)



