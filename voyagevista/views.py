from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment, Rating
from django.core.paginator import Paginator
from .forms import CommentForm, PostForm, RatingForm
from django.http import JsonResponse
import json
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db.models import Avg
from django.db import IntegrityError


def category_view(request, category_slug=None):
    """
    View for displaying posts filtered by category.
    """
    category = None
    categories = Category.objects.all()
    posts = Post.objects.filter(status=1).order_by('-created_on')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
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


class PostDetailView(View):
    def get(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        selected_post.number_of_views += 1  # Increment the number of views
        selected_post.save()

        approved_comments = selected_post.comments.filter(approved=True)
        pending_comments = []

        if request.user.is_authenticated:
            pending_comments = selected_post.comments.filter(approved=False, author=request.user)
            user_rating = selected_post.ratings.filter(user=request.user).first()
            is_bookmarked = selected_post.saves.filter(id=request.user.id).exists()
        else:
            user_rating = None
            is_bookmarked = False
            rating_form_instance = RatingForm()

        is_liked = selected_post.likes.filter(id=request.user.id).exists()

        comments_with_info = []
        for comment in approved_comments:
            is_owner = comment.author.username.lower() == request.user.username.lower()
            comments_with_info.append({"mycomment": comment, "is_owner": is_owner})

        comment_form_instance = CommentForm()
        rating_form_instance = RatingForm(instance=user_rating)

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'awaiting_comments': pending_comments,
            'comment_form': comment_form_instance,
            'rating_form': rating_form_instance,
            'liked': is_liked,
            'is_post_user': (request.user.id == selected_post.author.id),
            'is_bookmarked': is_bookmarked,
        })

    def post(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        approved_comments = selected_post.comments.filter(approved=True)

        if 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            selected_comment = get_object_or_404(Comment, id=comment_id)
            comment_form_instance = CommentForm(request.POST, instance=selected_comment)
            if comment_form_instance.is_valid():
                comment_form_instance.save()
                messages.success(request, 'Comment updated successfully.')
            else:
                messages.error(request, 'Error updating comment.')

        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            selected_comment = get_object_or_404(Comment, id=comment_id)
            selected_comment.delete()
            messages.success(request, 'Comment deleted successfully.')
        
        elif 'submit_rating' in request.POST:
            rating_form_instance = RatingForm(request.POST)
            if rating_form_instance.is_valid():
                rating, created = Rating.objects.update_or_create(
                    user=request.user,
                    post=selected_post,
                    defaults={'rating': rating_form_instance.cleaned_data['rating']},
                )
                messages.success(request, 'Rating submitted successfully.')

                return JsonResponse({'success': True, 'message': 'Rating submitted successfully'})
            else:
                messages.error(request, 'Error submitting rating.')
                return JsonResponse({'success': False, 'error': 'Error submitting rating'})

        else:
            comment_form_instance = CommentForm(request.POST)
            if comment_form_instance.is_valid():
                comment = comment_form_instance.save(commit=False)
                comment.author = request.user
                comment.post = selected_post
                comment.save()
                is_bookmarked = False
                messages.success(request, 'Your comment has been submitted for approval.')
                return HttpResponseRedirect(reverse('post_detail', args=[slug]))

        comments_with_info = []
        for comment in approved_comments:
            is_owner = comment.author.username.lower() == request.user.username.lower()
            comments_with_info.append({"mycomment": comment, "is_owner": is_owner})

        is_liked = selected_post.likes.filter(id=request.user.id).exists()
        is_bookmarked = selected_post.saves.filter(id=request.user.id).exists()

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'comment_form': comment_form_instance,
            'liked': is_liked,
            'is_post_user': (request.user.id == selected_post.author.id),
            'is_bookmarked': is_bookmarked,
            'rating_form': rating_form_instance,
        })

@method_decorator(login_required, name='dispatch')
class PostBookmark(View):
    """
    View class to handle bookmarking/unbookmarking of posts by users.
    """
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if post.saves.filter(id=request.user.id).exists():
            post.saves.remove(request.user)
            messages.success(request, 'Bookmark removed.')
        else:
            post.saves.add(request.user)
            messages.success(request, 'Post bookmarked.')

        return redirect('post_detail', slug=slug)

@method_decorator(login_required, name='dispatch')
class CommentEdit(View):
    def get(self, request, slug=None, pk=None, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        selected_comment = get_object_or_404(Comment, pk=pk, post=selected_post)
        if request.user.id != selected_comment.author.id:
            messages.error(request, 'You do not have permission to edit this comment.')
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        return render(request, "update_comment.html", {
            "status_message": "",
            "post": selected_post,
            "comment_form": CommentForm(instance=selected_comment),
        })

    def post(self, request, slug=None, pk=None, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        selected_comment = get_object_or_404(Comment, pk=pk, post=selected_post)
        if request.user.id != selected_comment.author.id:
            return JsonResponse({'success': False, 'error': 'You do not have permission to edit this comment.'})

        comment_form_instance = CommentForm(data=request.POST, instance=selected_comment)
        if comment_form_instance.is_valid():
            comment_form_instance.save()
            return JsonResponse({'success': True, 'message': 'Comment updated successfully.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid input.'})
        
        messages.error(request, 'Invalid input.')
        return render(request, "update_comment.html", {
            "comment_form": comment_form_instance,
            "post": selected_post,
        })
        
@method_decorator(login_required, name='dispatch')
class CommentDeleteView(View):
    def get(self, request, slug=None, pk=None, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        comment_queryset = selected_post.comments.filter(pk=pk)
        selected_comment = get_object_or_404(comment_queryset)
        if request.user.id != selected_comment.author.id:
            messages.error(request, 'You do not have permission to delete this comment.')
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        if selected_comment.delete():
            messages.success(request, "Comment Deleted Successfully")
            return redirect("post_detail", slug=slug)
        else:
            messages.error(request, "Comment Deletion Failed!")
        approved_comments = selected_post.comments.filter(approved=True).order_by("-created_on")
        is_liked = selected_post.likes.filter(id=request.user.id).exists()
        return render(request, "post_detail.html", {
            "is_post_user": (request.user.id == selected_post.author.id),
            "status_message": "Comment Deletion Failed!",
            "post": selected_post,
            "comments": approved_comments,
            "commented": False,
            "liked": is_liked,
            "comment_form": CommentForm(),
        })

@method_decorator(login_required, name='dispatch')
class PostLike(View):
    """
    View class to handle post likes/unlikes.
    """
    def post(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        if selected_post.likes.filter(id=request.user.id).exists():
            selected_post.likes.remove(request.user)
        else:
            selected_post.likes.add(request.user)
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))

@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    """
    View class to handle deleting user's own posts.
    """
    def get(self, request, slug=None, *args, **kwargs):
        selected_post = get_object_or_404(Post.objects.filter(status=1), slug=slug)
        if request.user.id == selected_post.author.id:
            selected_post.delete()
            return redirect("home")
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))

class MyLikesView(LoginRequiredMixin, ListView):
    """
    View class to display a list of posts that the current user has liked.
    """
    model = Post
    template_name = 'my_likes.html'
    context_object_name = 'liked_posts'

    def get_queryset(self):
        return self.request.user.blog_likes.all()

class MyCommentsView(LoginRequiredMixin, ListView):
    """
    View class to display a list of posts that current user has commented.
    """
    model = Comment
    template_name = 'my_comments.html'
    context_object_name = 'user_comments'

    def get_queryset(self):
        return self.request.user.commenter.all()

class MyBookmarksView(LoginRequiredMixin, TemplateView):
    """
    View class to display a list of posts that current user has bookmarked.
    """
    template_name = 'my_bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_bookmarks'] = self.request.user.blog_saves.all()
        return context

class AddPostView(LoginRequiredMixin, CreateView):
    """
    View class to handle the creation of new posts by authenticated users.
    """
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def rate_post(request, post_slug):
    """
    View function to handle rating of posts by authenticated users via JSON POST requests.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating_value = data.get('rating')
            
            # Validate rating value
            if rating_value is None or not (1 <= rating_value <= 5):
                return JsonResponse({'success': False, 'error': 'Invalid rating value.'}, status=400)
            
            # Get user and post objects
            user = request.user
            post = get_object_or_404(Post, slug=post_slug)

            # Create or get existing rating object
            rating, created = Rating.objects.get_or_create(user=user, post=post, defaults={'rating': 0})

            # Update the rating value
            rating.rating = rating_value
            rating.save()

            # Calculate average rating
            average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']
            post.average_rating = average_rating
            post.save()

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False}, status=400)