from django.core.management.base import BaseCommand
from voyagevista.models import Post
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Generate slugs for posts without slugs'

    def handle(self, *args, **kwargs):
        posts_without_slug = Post.objects.filter(slug__isnull=True) | Post.objects.filter(slug__exact='')
        for post in posts_without_slug:
            post.slug = slugify(post.title) or str(uuid.uuid4())
            post.save()
        self.stdout.write(self.style.SUCCESS('Successfully generated slugs for posts'))