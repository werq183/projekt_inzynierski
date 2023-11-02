import string
import random
from random import choice, sample

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from .models import Artist, Image

from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.generic import CreateView

from .forms import CustomAuthenticationForm, CustomUserCreationForm, UserProfileForm, ImageSearchForm

'''def index(request):
    return HttpResponse("Hello, world. You're at the app index.")'''


def home(request):
    images = Image.objects.order_by('?')[:5]
    return render(request, "home.html", {'images': images})


def artists(request):
    queryset = Artist.objects.all()
    context = {"photos": queryset}
    return render(request, "artists.html", context)


def artist_detail(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    return render(request, 'artist-detail.html', {'artist': artist})


def password(request):
    if request.method == "POST":
        length = int(request.POST.get("length"))
        uppercase = request.POST.get("uppercase")
        symbols = request.POST.get("symbols")
        numbers = request.POST.get("numbers")
        lowercase = request.POST.get("lowercase")
        chars = []
        if lowercase:
            chars.extend(string.ascii_lowercase)
        if uppercase:
            chars.extend(string.ascii_uppercase)
        if symbols:
            chars.extend("!@#$%^&*")
        if numbers:
            chars.extend("1234567890")
        generated_PASS = ""
        if numbers or lowercase or symbols or uppercase:
            for x in range(length):
                generated_PASS += choice(chars)
        else:
            generated_PASS = "zaznacz cos wrr"
        return JsonResponse({"password": generated_PASS})


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"

    def get_success_url(self):
        return reverse("signin")


class SignIn(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "signin.html"

    def get_success_url(self):
        return reverse("home")


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    is_owner = request.user == user

    if request.method == 'POST' and is_owner:
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dane zaktualizowane pomyślnie.')
            new_username = form.cleaned_data['username']
            return redirect('user_profile', username=new_username)
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'profile.html', {'form': form, 'is_owner': is_owner, 'target_user': user})


def logout_view(request):
    logout(request)
    return render(request, 'logged-out.html')


def image_search(request):
    images = list(Image.objects.all())  # Convert QuerySet to list

    if request.method == "POST":
        form = ImageSearchForm(request.POST)
        if form.is_valid():
            artists = form.cleaned_data['artists']
            subjects = form.cleaned_data['subjects']

            if artists and subjects:
                images = Image.objects.filter(style__in=artists, subject__in=subjects)
            else:
                messages.error(request, 'Proszę wybrać zarówno artystę, jak i temat.')
                images = []
        else:
            random.shuffle(images)
            images = images[:6]
    else:
        form = ImageSearchForm()
        random.shuffle(images)
        images = images[:6]

    context = {
        'form': form,
        'images': images
    }

    return render(request, 'img-search.html', context)

