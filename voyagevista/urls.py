from . import views
from django.urls import path
from .views import AddPostView, MyLikesView, MyCommentsView, MyBookmarksView, CommentEdit, CommentDeleteView, EditPostView, DeletePostView, MyPostsView, SearchPostListView, HomeView, PostDetailView, PostLike, PostBookmark, rate_post


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('add-post/', AddPostView.as_view(), name='add_post'),
    path('post/<slug:slug>/like/', PostLike.as_view(), name='post_like'),
    path('comment/<slug:slug>/<int:pk>/edit/', CommentEdit.as_view(), name='edit_comment'),
    path('comment/<slug:slug>/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete_comment'),
    path('post/<slug:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('my-likes/', MyLikesView.as_view(), name='my_likes'),
    path('my-comments/', MyCommentsView.as_view(), name='my_comments'),
    path('my-bookmarks/', MyBookmarksView.as_view(), name='my_bookmarks'),
    path('post/<slug:slug>/bookmark/', PostBookmark.as_view(), name='post_bookmark'),
    path('rate-post/<slug:post_slug>/', views.rate_post, name='rate_post'),
    path('post/<slug:slug>/edit/', EditPostView.as_view(), name='edit_post'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
]