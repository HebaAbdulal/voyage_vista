from . import views
from django.urls import path


urlpatterns = [
    path('', views.category_view, name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('comment/<int:id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:id>/delete/', views.delete_comment, name='delete_comment'),
]