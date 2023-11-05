
from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm,
                                       UsernameField)

from .models import User, Artist, Subject


class CustomUserCreationForm(UserCreationForm):
    username = UsernameField(
        label="Nazwa użytkownika",
        help_text="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nazwa użytkownika",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        help_text="",
        widget=forms.EmailInput(attrs={"placeholder": "Email"}),
    )
    password1 = forms.CharField(
        label="Hasło",
        help_text="",
        widget=forms.PasswordInput(attrs={"placeholder": "Hasło"}),
    )
    password2 = forms.CharField(
        label="Powtórz hasło",
        help_text="",
        widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło"}),
    )
    birth_date = forms.DateField(
        label="Data urodzenia",
        help_text="",
        widget=forms.DateInput(attrs={"type": "date", "placeholder": "Data urodzenia"}),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "birth_date")
        widgets = {}
        help_texts = {
            "username": None,
            "email": None,
            "password1": None,
            "password2": None,
        }
        label = {
            "username": "Nazwa użytkownika",
            "email": "Email",
            "password1": "Hasło",
            "password2": "Powtórz hasło",
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label="Nazwa użytkownika", help_text="", widget=forms.TextInput
    )
    password = forms.CharField(label="Hasło", help_text="", widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "Nazwa użytkownika lub hasło są niepoprawne.",
        "inactive": "Konto jest nieaktywne.",
    }

    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "username": None,
            "password": None,
        }
        label = {
            "username": "Nazwa użytkownika",
            "password": "Hasło",
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Użytkownik o tej nazwie już istnieje.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Użytkownik z tym adresem e-mail już istnieje.')
        return email


class ImageSearchForm(forms.Form):
    artists = forms.ModelMultipleChoiceField(
        queryset=Artist.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

