from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment, Rating
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
from django.db.models import Q


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
    

class HomeView(generic.ListView):
    """
    View for displaying a list of published posts.
    """
    queryset = Post.objects.filter(status=1)
    template_name = "index.html"
    paginate_by = 4


class PostDetailView(View):
    def get(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        selected_post.number_of_views += 1
        selected_post.save()

        approved_comments = selected_post.comments.filter(approved=True)
        pending_comments = selected_post.comments.filter(approved=False, author=request.user) if request.user.is_authenticated else []

        user_rating = selected_post.ratings.filter(user=request.user).first() if request.user.is_authenticated else None
        is_bookmarked = selected_post.saves.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        is_liked = selected_post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False

        comments_with_info = [{"mycomment": comment, "is_owner": comment.author == request.user} for comment in approved_comments]

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'awaiting_comments': pending_comments,
            'comment_form': CommentForm(),
            'rating_form': RatingForm(instance=user_rating),
            'liked': is_liked,
            'is_post_user': request.user == selected_post.author,
            'is_bookmarked': is_bookmarked,
        })

    def post(self, request, slug):
        selected_post = get_object_or_404(Post, slug=slug)
        approved_comments = selected_post.comments.filter(approved=True).order_by("-created_on")

        if 'edit_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            selected_comment = get_object_or_404(Comment, id=comment_id)
            comment_form_instance = CommentForm(request.POST, instance=selected_comment)
            if comment_form_instance.is_valid():
                edited_comment = comment_form_instance.save(commit=False)
                edited_comment.approved = False
                edited_comment.save()
                messages.success(request, 'Comment updated successfully and is now awaiting approval.')
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
                messages.success(request, 'Your comment has been submitted for approval.')
                return HttpResponseRedirect(reverse('post_detail', args=[slug]))

        comments_with_info = [{"mycomment": comment, "is_owner": comment.author == request.user} for comment in approved_comments]
        is_liked = selected_post.likes.filter(id=request.user.id).exists()
        is_bookmarked = selected_post.saves.filter(id=request.user.id).exists()

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_with_info,
            'comment_form': comment_form_instance,
            'liked': is_liked,
            'is_post_user': request.user == selected_post.author,
            'is_bookmarked': is_bookmarked,
            'rating_form': RatingForm(instance=selected_post.ratings.filter(user=request.user).first()),
            'commented': request.user.is_authenticated and selected_post.comments.filter(author=request.user).exists(),
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
            edited_comment = comment_form_instance.save(commit=False)
            edited_comment.approved = False  # Set the comment to awaiting approval
            edited_comment.save()
            return JsonResponse({'success': True, 'message': 'Comment updated successfully and is now awaiting approval.'})
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

    def post(self, request, slug=None, pk=None, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        selected_comment = get_object_or_404(Comment, pk=pk, post=selected_post)
        
        if request.user.id != selected_comment.author.id:
            messages.error(request, 'You do not have permission to delete this comment.')
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))
        
        selected_comment.delete()
        messages.success(request, "Comment Deleted Successfully")
        return redirect("post_detail", slug=slug)


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
    def get(self, request, slug=None, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug)
        if request.user.id == selected_post.author.id:
            selected_post.delete()
            messages.success(request, 'Post deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
    
    def post(self, request, slug, *args, **kwargs):
        selected_post = get_object_or_404(Post, slug=slug)
        if request.user == selected_post.author:
            selected_post.delete()
            messages.success(request, 'Post deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            return redirect(reverse('post_detail', args=[slug]))


class MyLikesView(LoginRequiredMixin, ListView):
    """
    View class to display a list of posts that the current user has liked.
    """
    model = Post
    template_name = 'my_likes.html'
    context_object_name = 'liked_posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Access the related posts via the user relationship
        liked_posts = self.request.user.blog_likes.all()

        paginator = Paginator(liked_posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)

        context['liked_posts'] = posts_page
        context['page_obj'] = posts_page

        return context


class MyCommentsView(LoginRequiredMixin, ListView):
    """
    View class to display a list of posts that the current user has commented on.
    """
    model = Comment
    template_name = 'my_comments.html'
    context_object_name = 'user_comments'
    paginate_by = 4

    def get_queryset(self):
        return self.request.user.commenter.all()


class MyBookmarksView(LoginRequiredMixin, TemplateView):
    """
    View class to display a list of posts that current user has bookmarked.
    """
    template_name = 'my_bookmarks.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Access the related posts via the user relationship
        bookmarked_posts = self.request.user.blog_saves.all()

        paginator = Paginator(bookmarked_posts, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)

        context['bookmarked_posts'] = posts_page
        context['page_obj'] = posts_page

        return context


class MyPostsView(LoginRequiredMixin, TemplateView):
    """
    View class to display a list of posts that current user has created, categorized by their approval status.
    """
    template_name = 'my_posts.html'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_posts = self.request.user.blog_posts.all()
        
        approved_posts = user_posts.filter(approved=True)
        pending_posts = user_posts.filter(approved=False)

        paginator_approved = Paginator(approved_posts, self.paginate_by)
        paginator_pending = Paginator(pending_posts, self.paginate_by)
        
        page = self.request.GET.get('page')

        try:
            approved_page = paginator_approved.page(page)
        except PageNotAnInteger:
            approved_page = paginator_approved.page(1)
        except EmptyPage:
            approved_page = paginator_approved.page(paginator_approved.num_pages)

        try:
            pending_page = paginator_pending.page(page)
        except PageNotAnInteger:
            pending_page = paginator_pending.page(1)
        except EmptyPage:
            pending_page = paginator_pending.page(paginator_pending.num_pages)

        context['approved_posts'] = approved_page
        context['pending_posts'] = pending_page
        context['approved_page_obj'] = approved_page
        context['pending_page_obj'] = pending_page

        return context

        
class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 0
        response = super().form_valid(form)
        messages.success(self.request, 'Your post is awaiting approval.')
        return redirect(self.success_url)


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


@method_decorator(login_required, name='dispatch')
class EditPostView(View):
    success_url = 'post_detail'  # Ensure this URL name exists in your urls.py

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author or request.user.is_superuser:
            form = PostForm(instance=post)
            return render(request, 'edit_post.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You do not have permission to edit this post.')
            return redirect('post_detail', slug=slug)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author or request.user.is_superuser:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                edited_post = form.save(commit=False)
                edited_post.approved = False  # Set post to awaiting approval
                edited_post.status = 0  # Set post status to Draft
                edited_post.save()
                messages.success(request, 'Post updated successfully and is now awaiting approval.')
                return redirect(self.success_url, slug=slug)  # Redirect to the post detail view
            else:
                messages.error(request, 'Invalid input.')
        return render(request, 'edit_post.html', {'form': form, 'post': post})

        
class SearchPostListView(ListView):
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context