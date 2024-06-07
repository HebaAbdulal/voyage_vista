from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Form for submitting comments on posts.
    """
    class Meta:
        model = Comment
        fields = ('body', 'author',)