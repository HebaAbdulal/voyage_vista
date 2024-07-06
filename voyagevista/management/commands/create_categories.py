from django.core.management.base import BaseCommand
from voyagevista.models import Category

class Command(BaseCommand):
    help = 'Create default categories'

    def handle(self, *args, **kwargs):
        categories = ['Destinations', 'Travel Tips', 'Accommodation']
        for category_name in categories:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created category: {category_name}'))
            else:
                self.stdout.write(f'Category {category_name} already exists')
