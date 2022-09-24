from unicodedata import name
from django.shortcuts import render


def home(request):
    return render(request, "main/home.html")
