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
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, approved=True)
    awaiting_comments = Comment.objects.filter(post=post, approved=False, author=request.user)
    comment_form = CommentForm(request.POST or None)

    if request.method == 'POST':
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.is_ajax():
                return JsonResponse({
                    'id': comment.id,
                    'name': comment.author.username,
                    'created_on': comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                    'body': comment.body
                })
            else:
                return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'comments': comments,
        'awaiting_comments': awaiting_comments,
        'comment_form': comment_form,
    }
    return render(request, 'post_detail.html', context)

@csrf_exempt
def edit_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            new_body = request.POST.get('body')
            if new_body:
                comment.body = new_body
                comment.save()
                return JsonResponse({'success': True})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id, author=request.user)
            comment.delete()
            return JsonResponse({'success': True})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
