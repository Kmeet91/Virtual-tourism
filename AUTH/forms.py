from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your forms here.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
from django import forms
from .models import Subscription
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
User = get_user_model()

from django import forms
from .models import Subscription
from django.utils.timezone import now, timedelta

@login_required
class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']

    def save(self, commit=True):
        """Save the subscription with a default validity period (e.g., 1 year)"""
        subscription = super().save(commit=False)
        subscription.valid_until = now() + timedelta(days=365)  # 1 year validity
        if commit:
            subscription.save()
        return subscription
    
    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

# users/forms.py
from django import forms
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

from django import forms
from .models import Profile

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'birth_date', 'gender', 'country_code', 'phone_number','house_no','address', 'city', 'zip']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'dd/mm/yyyy'}),
        }
        
    def save(self, commit=True):
        """Custom save method to update the Profile instance properly"""
        profile = super().save(commit=False)

        # Additional processing logic can go here (e.g., setting default values)

        if commit:
            profile.save()  # Save to database
        return profile


def form_validation_error(form):
    msg = ""
    for field in form:
        for error in field.errors:
            msg += "%s: %s \\n" % (field.label if hasattr(field, 'label') else 'Error', error)
    return msg


