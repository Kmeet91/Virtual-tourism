from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
app_name = "main"

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('destination/<int:id>/', views.destination_detail, name='destination_detail'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('toggle_bookmark/<int:id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('upload_image/<int:id>/', views.upload_image, name='upload_image'),  # Ensure this path exists
    path('destination/<int:destination_id>/submit-review/', views.submit_review, name='submit_review'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
