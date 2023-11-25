import json
import string
import random
import requests
from random import choice, sample

from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Artist, Image, UserImagePreferences
from django.conf import settings
from django.contrib.auth.views import LoginView
from asgiref.sync import async_to_sync
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.generic import CreateView

from django.http import JsonResponse
import httpx
import asyncio

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
    form = UserProfileForm(instance=user)  # Define form here for GET requests
    password_form = PasswordChangeForm(user)  # Define password_form here for GET requests

    if request.method == 'POST' and is_owner:
        if 'update_profile' in request.POST:
            form = UserProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Dane zaktualizowane pomyślnie.')
                new_username = form.cleaned_data.get('username')
                if new_username and new_username != username:
                    return redirect('user_profile', username=new_username)
                else:
                    return redirect('user_profile', username=username)
            else:
                messages.error(request, 'Proszę poprawić błędy w formularzu.')
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in
                messages.success(request, 'Twoje hasło zostało zaktualizowane!')
                return redirect('user_profile', username=username)
            else:
                messages.error(request, 'Popraw błędy w formularzu zmiany hasła.')

    # If it's a GET request or there's some error
    return render(request, 'profile.html', {
        'form': form,
        'password_form': password_form,
        'is_owner': is_owner,
        'target_user': user
    })


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


async def send_async_request(api_url, payload, headers):
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=payload, timeout=3600)
        return response


async def generate_image(request):
    images = []
    form_submitted = False  # zmienna śledząca, czy formularz został wysłany

    def get_preferences_if_authenticated(user):
        if user.is_authenticated:
            try:
                return UserImagePreferences.objects.filter(user=user)
            except UserImagePreferences.DoesNotExist:
                return None
        else:
            return None

    def create_preferences(user, prompt, negative_prompt, seed, height, width, steps):
        UserImagePreferences.objects.create(
            user=user,
            prompt=prompt,
            negative_prompt=negative_prompt,
            seed=seed,
            height=height,
            width=width,
            steps=steps
        )
    saved_preferences = await sync_to_async(get_preferences_if_authenticated)(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')
        prompt = request.POST.get('prompt')
        negative_prompt = request.POST.get('negative_prompt')
        if negative_prompt is None:
            negative_prompt = ""
        number_of_images = int(request.POST.get('number_of_images', 1))
        number_of_images = max(1, min(number_of_images, 10))  # Ogranicz zakres od 1 do 10
        width = int(request.POST.get('width', 512))  # get width from POST data with default value
        width = max(256, min(width, 1024))
        height = int(request.POST.get('height', 512))  # get height from POST data with default value
        height = max(256, min(height, 1024))
        steps = int(request.POST.get('steps', 20))  # get steps from POST data
        seed = int(request.POST.get('seed', 1))

        if action == 'save':
            await sync_to_async(create_preferences)(user=request.user, prompt=prompt, negative_prompt=negative_prompt, seed=seed, height=height, width=width, steps=steps)

        elif action == 'generate':
            form_submitted = True
            # URL do API Stable Diffusion
            # api_url = 'http://vpn.skmiec.pl:47861'
            # api_url = 'http://10.0.10.30:7861'
            api_url = 'http://185.153.36.169:62137'
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "width": width,
                "height": height,
                "steps": steps,
                "guidance_scale": 7.5,
                "safety_checker": True,
                "seed": seed,
                "subseed": 1
            }

            for _ in range(number_of_images):
                response = await send_async_request(api_url + '/sdapi/v1/txt2img', payload, headers)
                if response.status_code == 200:
                    response_data = response.json()
                    if 'images' in response_data:
                        images.append('data:image/png;base64,' + response_data['images'][0])
                    else:
                        error = response_data.get('error', 'Odpowiedź API nie zawiera oczekiwanych danych.')
                        content = await sync_to_async(render)(request, 'generate_image.html', {'error': error})
                        return HttpResponse(content.content)
                else:
                    error = "Wystąpił błąd przy generowaniu obrazu."
                    if response.json():
                        error = response.json().get('error', error)
                    content = await sync_to_async(render)(request, 'generate_image.html', {'error': error})
                    return HttpResponse(content.content)
            content = await sync_to_async(render)(request, 'generate_image.html', {
                'images_urls': images,
                'form_submitted': form_submitted,
                'saved_preferences': saved_preferences
            })
            return HttpResponse(content.content)
    else:
        # domyślne wartości dla formularza
        prompt = "Tu wpisz swoje zapytanie"
        negative_prompt = "ugly, deformed, poor quality"
        number_of_images = 1
        width = 512
        height = 512
        steps = 20
        seed = 1
    context = {
        'user': request.user,
        'images_urls': images,
        'prompt': prompt,
        'negative_prompt': negative_prompt,
        'number_of_images': number_of_images,
        'width': width,
        'height': height,
        'steps': steps,
        'seed': seed,
        'saved_preferences': saved_preferences
    }
    content = await sync_to_async(render)(request, 'generate_image.html', context)
    return HttpResponse(content.content)


async def delete_preference(request, preference_id):
    if request.method != 'DELETE':
        return HttpResponseNotAllowed(['DELETE'])
    try:
        # Retrieve the preference asynchronously
        preference = await sync_to_async(UserImagePreferences.objects.get, thread_sensitive=True)(id=preference_id, user=request.user)
        # Delete the preference asynchronously
        await sync_to_async(preference.delete, thread_sensitive=True)()
        return JsonResponse({'status': 'success'}, status=204)
    except UserImagePreferences.DoesNotExist:
        return JsonResponse({'error': 'Preference not found'}, status=404)
    except Exception as e:
        # It's a good practice to log the exception here
        print(str(e))
        return JsonResponse({'error': str(e)}, status=500)

