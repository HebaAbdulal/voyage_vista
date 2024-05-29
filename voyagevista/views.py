from django.shortcuts import render
from voyagevista.models import Item

def home_view(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'main/home.html', context)

# Create your views here.
