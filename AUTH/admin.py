from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Subscription, Profile

User = get_user_model()

# Custom UserAdmin for better user management
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

# Register the custom User model
admin.site.register(User, CustomUserAdmin)

# Custom SubscriptionAdmin for better subscription management
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'subscribed_at', 'valid_until')
    search_fields = ('user__username', 'email')
    ordering = ('user__username',)
    autocomplete_fields = ('user',)
    list_filter = ('user','subscribed_at', 'valid_until')

# Register the Subscription model with the custom admin
admin.site.register(Subscription, SubscriptionAdmin)

# Profile model admin configuration
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'city')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('user','city',)
    autocomplete_fields = ('user',)

# Register the Profile model
admin.site.register(Profile, ProfileAdmin)