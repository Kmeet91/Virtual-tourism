from django.urls import path
from . import views
from .views import subscription_view
from django.contrib.auth import get_user_model
from django.conf.urls.static import static
from django.conf import settings
User = get_user_model()

app_name = "AUTH"

urlpatterns = [
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("", views.home, name="home"),
    path("logout", views.logout_request, name="logout"),
    path('subscribe', views.subscription_view, name='subscribe'),  # Subscription page
    path('profile/', views.profile, name='profile'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
