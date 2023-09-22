from django.http import HttpResponse
from django.shortcuts import render


'''def index(request):
    return HttpResponse("Hello, world. You're at the app index.")'''


def home(request):
    return render(request, "home.html")