from . import views
from django.urls import path


urlpatterns = [
    path('', views.category_view, name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
     path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]