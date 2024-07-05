from . import views
from django.urls import path


urlpatterns = [
    path('', views.category_view, name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/like/', views.PostLike.as_view(), name='post_like'),
    path('comment/<slug:slug>/<int:pk>/edit/', views.CommentEdit.as_view(), name='edit_comment'),
    path('comment/<slug:slug>/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
    path('post/<slug:slug>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('my-likes/', MyLikesView.as_view(), name='my_likes'),
    path('my-comments/', MyCommentsView.as_view(), name='my_comments'),
    path('my-bookmarks/', MyBookmarksView.as_view(), name='my_bookmarks'),
    path('rate-post/<slug:post_slug>/', views.rate_post, name='rate_post'),
    path('post/<slug:slug>/bookmark/', views.PostBookmark.as_view(), name='post_bookmark'),
]