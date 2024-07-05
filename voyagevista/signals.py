from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rating, Post

@receiver(post_save, sender=Rating)
def update_post_rating_on_rating_save(sender, instance, created, **kwargs):
    """
    Signal handler to update the average rating of a Post when a Rating instance is saved.
    """
    post = instance.post
    ratings = Rating.objects.filter(post=post)
    sum_ratings = sum([rating.rating for rating in ratings])  # Ensure this is the correct field name
    count_ratings = ratings.count()
    average_rating = sum_ratings / count_ratings if count_ratings > 0 else 0
    post.average_rating = average_rating
    post.save()