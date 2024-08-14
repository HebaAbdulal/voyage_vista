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
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'excerpt', 'category']

    def save(self, commit=True):
        post = super().save(commit=False)
        post.approved = False  # Set approved to False by default
        if commit:
            post.save()
        return post

class RatingForm(forms.ModelForm):
    """
    Form class for handling rating submissions.
    """
    class Meta:
        model = Rating
        fields = ['rating']


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)