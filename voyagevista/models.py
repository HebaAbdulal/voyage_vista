from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.utils.text import slugify
import uuid

# Create your models here.
STATUS = ((0, "Draft"), (1, "Published"))


class Category(models.Model):
    """
    Model representing a category for the blog posts.

    Attributes:
        name (CharField): The name of the category.
        slug (SlugField): The slug for the category.
    """
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Model representing a blog post.
    """

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    saves = models.ManyToManyField(User, related_name='blog_saves', blank=True)
    approved = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_views = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """
        Returns the total number of likes for the post.
        """
        return self.likes.count()

    def number_of_saves(self):
        """
        Returns the total number of saves for the post.
        """
        return self.saves.count()

    def average_rating(self):
        """
        Alias for calculate_average_rating method.
        Deprecated in favor of calculate_average_rating.
        """
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) or str(uuid.uuid4())
        super().save(*args, **kwargs)

    def number_of_comments(self):
        return self.comments.filter(approved=True).count()


class Comment(models.Model):
    """
    Model representing a comment on a post.
    """
    post = models.ForeignKey(
            Post, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter", default=1)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    content = models.TextField(default="Default content")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"comment {self.body} by {self.author.username}"

    def number_of_comments(self):
        """
        Returns the total number of comments for the post.
        """
        return self.comments.filter(approved=True).count()

    class Meta:
        ordering = ['created_on']


class Rating(models.Model):
    """
    Model representing a rating on post
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user} - {self.post} - {self.rating}"
