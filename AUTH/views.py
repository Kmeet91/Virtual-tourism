from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from .forms import NewUserForm, SubscriptionForm, ProfileForm
from django.conf import settings
from .models import Subscription, Profile
from main.models import Destination

# Get the custom user model
User = get_user_model()


def home(request):
    return render(request, 'home.html')


# 🔹 User Registration View
def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AUTH:login')
    else:
        form = NewUserForm()
    return render(request, 'AUTH/register.html', {'form': form,'media_url': settings.MEDIA_URL})

# 🔹 User Login View
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                next_url = request.POST.get('next') or 'main:home'
                return redirect(next_url)
            else:   
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "AUTH/login.html", {"form": form,'media_url': settings.MEDIA_URL})


# 🔹 User Logout View
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:home")


# 🔹 Subscription View
@login_required
def subscription_view(request):
    user = request.user  # Custom User model instance

    if request.method == "POST":
        email = request.POST.get('email')  # Get the email from the form
        plan = request.POST.get('plan')  # Get the selected plan (monthly or yearly)

        # Validate the email (ensure it matches the logged-in user's email)
        if email != user.email:
            messages.error(request, "Invalid email address.")
            return redirect('AUTH:subscribe')

        # Set subscription validity based on the selected plan
        valid_until = now() + timedelta(days=30) if plan == 'monthly' else now() + timedelta(days=365)

        # Create or update the subscription
        subscription, created = Subscription.objects.get_or_create(user=user)
        subscription.email = email  # Explicitly set the email

        subscription.valid_until = valid_until  # Ensure valid_until is set
        subscription.save()

        messages.success(request, f"You have successfully subscribed to the {plan} plan!")
        next_url = request.POST.get('next') or 'main:home'
        return redirect(next_url)
    
    # Pre-fill the form with the logged-in user's email
    return render(request, 'AUTH/subscribe.html', {'user': user})


# 🔹 User Profile View
@login_required
def profile(request):
    user = request.user  # Custom User model instance
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        print("Form data received:", request.POST)  # Debugging
        print("Files received:", request.FILES)  # Debugging
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('AUTH:profile')
        else:
            print("Form errors:", form.errors)  # Debugging
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'AUTH/profile.html', {
        'form': form,
        'gender_choices': Profile.GENDER_CHOICES,
        'profile': profile
    })
