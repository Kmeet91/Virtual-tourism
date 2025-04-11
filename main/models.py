from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from AUTH.models import Profile  # Import Profile model


# Create your models here.
class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('beach', 'Beach'),
        ('heritage', 'Heritage'),
        ('wildlife', 'Wildlife'),
        ('religious', 'Religious'),
        ('adventure', 'Adventure'),
        ('hill_station', 'Hill Station'),
    ]
    
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    description = models.TextField(blank=True)  # Added description field
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='beach')
    popular = models.BooleanField(default=False)  # New field to mark popular destinations
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarked_destinations', blank=True)
    map_iframe_url = models.URLField(max_length=1000, blank=True, null=True)  # Storing Map iframe URL


    def __str__(self):
        return self.name


class Image(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='destination_images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Image for {self.destination.name}"

class View360(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='views_360')

    # Custom 360° Panorama Image
    panorama_image = models.ImageField(upload_to='360_views/', blank=True, null=True)

    # Store Google Maps iframe URL
    iframe_url = models.URLField(max_length=1000, blank=True, null=True, help_text="Google Maps Embed URL for Street View")

    def __str__(self):
        if self.iframe_url:
            return f"Embedded Street View for {self.destination.name}"
        elif self.panorama_image:
            return f"Custom 360 View for {self.destination.name}"
        else:
            return f"Invalid View for {self.destination.name} (No iframe or image)"

    def get_view_data(self):
        """
        Returns both the custom 360° panorama image URL and the Google Maps iframe URL (if available).
        """
        data = {}
        if self.panorama_image:
            data["custom_360_panorama"] = self.panorama_image.url
        if self.iframe_url:
            data["google_maps_embed"] = self.iframe_url
        return data



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name
    
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.destination.name}"