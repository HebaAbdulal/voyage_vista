from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.category_view, name='category'),
]