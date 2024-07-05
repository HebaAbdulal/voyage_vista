from django import forms
from .models import Comment, Post, Rating


class CommentForm(forms.ModelForm):
    """
    Form for submitting comments on posts.
    """
    class Meta:
        model = Comment
        fields = ('body',)

class PostForm(forms.ModelForm):
    """
    Form for submitting posts.
    """
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 'content', 'category', 'excerpt']

class RatingForm(forms.ModelForm):
    """
    Form class for handling rating submissions.
    """
    class Meta:
        model = Rating
        fields = ['rating']