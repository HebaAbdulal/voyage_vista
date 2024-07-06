from django.core.management.base import BaseCommand
from voyagevista.models import Rating
from django.db.models import Count

class Command(BaseCommand):
    help = 'Remove duplicate Rating entries'

    def handle(self, *args, **kwargs):
        duplicates = Rating.objects.values('user', 'post').annotate(count=Count('id')).filter(count__gt=1)
        for duplicate in duplicates:
            Rating.objects.filter(user=duplicate['user'], post=duplicate['post'])[1:].delete()
        self.stdout.write(self.style.SUCCESS('Successfully removed duplicate ratings'))