from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views
from .views import home, artists, galleries, SignIn, SignUp, password

urlpatterns = [
    path("", home, name="home"),
    path("artists/", artists, name="artists"),
    path("galleries/", galleries, name="galleries"),
    path("generate-password", password, name="password"),
    path("signup", SignUp.as_view(), name="signup"),
    path(
        "signin",
        SignIn.as_view(),
        name="signin",
    ),
    path("logout", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
