

# Create your views here.
from django.shortcuts import render
from .models import Post

from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html')


