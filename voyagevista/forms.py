from django import forms
from .models import Comment, Post, Rating, Category


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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user from kwargs
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        post.approved = False  # Set approved to False by default

        # Assign the author if it's not set
        if self.user:
            post.author = self.user

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

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError("Rating must be between 1 and 10.")
        return rating


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)
