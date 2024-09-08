from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Post, Category, Comment, Rating
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CommentForm, PostForm, RatingForm, ContactForm
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
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from django.conf import settings
from django.core.mail import EmailMessage
from django.views.generic.edit import CreateView


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
    """
    Handles the display of a single post's details, including comments, ratings, likes, and bookmarks.
    Supports editing and deleting comments, submitting ratings, and adding new comments.
    """
    def get(self, request, slug):
        """
        Display the post detail page, increment the view count, and retrieve user-specific data like 
        comments, ratings, likes, and bookmarks.
        """
        selected_post = get_object_or_404(Post, slug=slug)
        selected_post.number_of_views += 1
        selected_post.save()

        approved_comments = selected_post.comments.filter(approved=True)

        # Pagination
        paginator = Paginator(approved_comments, 5)  # Show 5 comments per page
        page_number = request.GET.get('page')
        comments_page = paginator.get_page(page_number)

        # Update the comments_with_info based on paginated comments
        comments_with_info = [{"mycomment": comment, "is_owner": comment.author == request.user} for comment in comments_page]

        # Fetch pending comments
        pending_comments = selected_post.comments.filter(approved=False, author=request.user) if request.user.is_authenticated else []

        user_rating = selected_post.ratings.filter(user=request.user).first() if request.user.is_authenticated else None
        is_bookmarked = selected_post.saves.filter(id=request.user.id).exists() if request.user.is_authenticated else False
        is_liked = selected_post.likes.filter(id=request.user.id).exists() if request.user.is_authenticated else False

        return render(request, 'post_detail.html', {
            'post': selected_post,
            'comments': comments_page,
            'comments_with_info': comments_with_info,
            'awaiting_comments': pending_comments,
            'comment_form': CommentForm(),
            'rating_form': RatingForm(instance=user_rating),
            'liked': is_liked,
            'is_post_user': request.user == selected_post.author,
            'is_bookmarked': is_bookmarked,
        })

    def post(self, request, slug):
        """
        Handle post-related actions such as editing/deleting comments, submitting ratings, and adding new comments.
        """
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
        """
        Render the edit comment form if the user is authorized to edit the comment.
        """
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        selected_comment = get_object_or_404(Comment, pk=pk, post=selected_post)
        if request.user.id != selected_comment.author.id:
            messages.error(request, 'You do not have permission to edit this comment.')
            return redirect('post_detail', slug=slug)

        # Include the comment form in the context
        context = {
            "status_message": "",
            "post": selected_post,
            "comment_form": CommentForm(instance=selected_comment),
            "awaiting_comments": Comment.objects.filter(post=selected_post, approved=False),
            "comments": Comment.objects.filter(post=selected_post, approved=True),
            "commented": False
        }
        return render(request, "post_detail.html", context)

    def post(self, request, slug=None, pk=None, *args, **kwargs):
        """
        Process the edit comment form submission and update the comment if valid.
        """
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

        
@method_decorator(login_required, name='dispatch')
class CommentDeleteView(View):
    """
    View to handle deletion of comments by authenticated users.
    """
    def get(self, request, slug=None, pk=None, *args, **kwargs):
        """
        Render the post detail page with a success or failure message.
        """
        selected_post = get_object_or_404(Post, slug=slug, status=1)
        comment_queryset = selected_post.comments.filter(pk=pk)
        selected_comment = get_object_or_404(comment_queryset)

        # Check if the current user is the author of the comment
        if request.user.id != selected_comment.author.id:
            messages.error(request, 'You do not have permission to delete this comment.')
            return HttpResponseRedirect(reverse("post_detail", args=[slug]))

        # Attempt to delete the comment
        selected_comment.delete()
        messages.success(request, "Comment Deleted Successfully")
        return redirect("post_detail", slug=slug)

    def post(self, request, slug=None, pk=None, *args, **kwargs):
        """
        Handle the POST request to delete a comment if the user has permission.
        """
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
            messages.info(request, "You have unliked the post.")
        else:
            selected_post.likes.add(request.user)
            messages.success(request, "You have liked the post.")
        return HttpResponseRedirect(reverse("post_detail", args=[slug]))


@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    """
    View to handle deletion of posts by authenticated users.
    """

    def post(self, request, slug=None, *args, **kwargs):
        """
        Handle POST request to delete a post if the user is authorized.
        """
        selected_post = get_object_or_404(Post, slug=slug)
        print(f"User: {request.user.id}, Post Author: {selected_post.author.id}")  # Debug print
        if request.user.id == selected_post.author.id:
            selected_post.delete()
            messages.success(request, 'Post deleted successfully.')
            print("Success message added")  # Debug print
            return redirect('home')
        else:
            messages.error(request, 'You do not have permission to delete this post.')
            print("Error message added")  # Debug print
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    
    
    def post(self, request, slug, *args, **kwargs):
        """
        Handle POST request to delete a post if the user is authorized.
        """
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
    ordering = ['-created_on']  # Ensure this is the correct field

    def get_queryset(self):
        return self.request.user.blog_likes.all().order_by('-created_on')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['liked_posts'] = page_obj
        context['page_obj'] = page_obj
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
    """
    View to handle the creation of new posts by authenticated users.
    """
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Set the post author and status, then save the post.
        """
        form.instance.author = self.request.user
        form.instance.status = 0  # Set post as 'awaiting approval'
        
        response = super().form_valid(form)
        messages.success(self.request, 'Your post is awaiting approval.')
        return response


@method_decorator(login_required, name='dispatch')
class RatePostView(View):
    def post(self, request, post_slug):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'User not authenticated.'}, status=401)

        try:
            data = json.loads(request.body)
            rating_value = data.get('rating')
            if rating_value is None or not (1 <= rating_value <= 5):
                return JsonResponse({'success': False, 'error': 'Invalid rating value.'}, status=400)

            user = request.user
            post = get_object_or_404(Post, slug=post_slug)

            rating, created = Rating.objects.get_or_create(user=user, post=post, defaults={'rating': rating_value})
            if not created:
                rating.rating = rating_value
                rating.save()

            average_rating = Rating.objects.filter(post=post).aggregate(Avg('rating'))['rating__avg']
            post.average_rating = average_rating
            post.save()

            # Include the success message in the JSON response
            return JsonResponse({
                'success': True, 
                'average_rating': average_rating, 
                'message': "You have rated the post successfully!"
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON.'}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
            

@method_decorator(login_required, name='dispatch')
class EditPostView(View):
    """
    View to handle editing of posts by authenticated users.
    """
    success_url = 'post_detail'

    def get(self, request, slug):
        """
        Render the edit post form if the user is authorized to edit the post.
        """
        post = get_object_or_404(Post, slug=slug)
        if request.user == post.author or request.user.is_superuser:
            form = PostForm(instance=post)
            return render(request, 'edit_post.html', {'form': form, 'post': post})
        else:
            messages.error(request, 'You do not have permission to edit this post.')
            return redirect('post_detail', slug=slug)

    def post(self, request, slug):
        """
        Process the edit post form submission and update the post if valid.
        """
        post = get_object_or_404(Post, slug=slug)
        
        # Initialize form for both valid and invalid cases
        form = PostForm(request.POST, request.FILES, instance=post)
        
        if request.user == post.author or request.user.is_superuser:
            if form.is_valid():
                edited_post = form.save(commit=False)
                edited_post.approved = False  # Set post to awaiting approval
                edited_post.status = 0  # Set post status to Draft
                edited_post.save()
                messages.success(request, 'Post updated successfully and is now awaiting approval.')
                return redirect(self.success_url, slug=slug)  # Redirect to the post detail view
            else:
                messages.error(request, 'Invalid input.')
        else:
            messages.error(request, 'You do not have permission to edit this post.')
            return redirect('post_detail', slug=slug)
        
        return render(request, 'edit_post.html', {'form': form, 'post': post})
        
        
class SearchPostListView(ListView):
    """
    View to display a list of posts matching a search query.
    """
    model = Post
    template_name = 'search_results.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        """
        Filter posts based on the search query.
        """
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        else:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        """
        Add the search query to the context data.
        """
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class ContactView(FormView):
    """
    View to handle contact form submissions.
    """
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        """
        Send an email with the contact form details and redirect to success page.
        """
        email = EmailMessage(
            subject=f"Contact Form Submission from {form.cleaned_data['name']}",
            body=form.cleaned_data['message'],
            from_email='hebaabdulal24@gmail.com',
            to=['hebaabdulal24@gmail.com'],
            reply_to=[form.cleaned_data['email']]  # User's email for replies
        )
        email.send(fail_silently=False)
        return super().form_valid(form)

        
class ContactSuccessView(TemplateView):
    """
    View to display the contact form submission success page.
    """
    template_name = 'contact_success.html'
    