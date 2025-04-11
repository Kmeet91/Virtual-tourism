# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User model extending Django's built-in User"""
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        """Ensure email uniqueness and save the user."""
        self.email = self.email.lower()  # Normalize email to lowercase
        super().save(*args, **kwargs)

    def is_subscribed(self):
        """Check if the user has an active subscription"""
        from AUTH.models import Subscription
        subscription = Subscription.objects.filter(email=self.email).first()
        return subscription and subscription.is_active()

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True, blank=True)  # Allow NULL values

    def __str__(self):
        return f"{self.email}"

    def is_active(self):
        """Check if the subscription is still valid"""
        return self.valid_until and self.valid_until > now()

class Profile(models.Model):
    GENDER_MALE = 1
    GENDER_FEMALE = 2
    GENDER_CHOICES = [
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    avatar = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True, default='')
    last_name = models.CharField(max_length=50, blank=True, null=True, default='')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    country_code = models.CharField(max_length=5, null=True, blank=True, default='+91')
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    house_no = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    zip = models.CharField(max_length=10, null=True, blank=True)

    def save(self, *args, **kwargs):
        """Custom save method to handle logic before saving the model."""
        if not self.avatar:
            self.avatar = 'profile_placeholder.png'  # Default avatar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal handler to create a Profile when a User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()