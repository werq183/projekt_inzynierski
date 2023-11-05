from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from . import views
from .views import home, artists, SignIn, SignUp, password, user_profile

urlpatterns = [
    path("", views.home, name="home"),
    path("artists/", artists, name="artists"),
    path('search/', views.image_search, name='search_images'),
    path('generate/', views.generate_image, name='generate_image'),
    path("generate-password", password, name="password"),
    path("signup", SignUp.as_view(), name="signup"),
    path("signin", SignIn.as_view(), name="signin"),
    path("logged-out/", LogoutView.as_view(template_name='logged-out.html'), name="logout_view"),
    path('artists/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
