from django.core.management.base import BaseCommand
from voyagevista.models import Category

class Command(BaseCommand):
    help = 'Update category slugs to use hyphens instead of underscores'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        for category in categories:
            category.slug = category.slug.replace('_', '-')
            category.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated slug for category: {category.name}'))