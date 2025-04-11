from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Destination, Contact, Image, View360
from AUTH.models import Profile
from .forms import ContactForm, ReviewForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render
from .models import Destination

def user_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return {'profile': profile}
    return {}

def home(request):
    popular_destinations = Destination.objects.filter(popular=True)  # Fetch only popular ones
    destinations = Destination.objects.all()  # Fetch all destinations
    return render(request, 'main/home.html', {
        'popular_destinations': popular_destinations,
        'destinations': destinations,
        'media_url': settings.MEDIA_URL
    })


def about(request):
    return render(request, 'main/about.html')

from django.shortcuts import render
from .models import Destination, Image

from django.shortcuts import render
from django.core.serializers import serialize
from .models import Destination, Image

from django.shortcuts import render
from .models import Destination, Image

def gallery(request):
    popular_destinations = Destination.objects.filter(popular=True)  # Fetch only popular ones
    destinations = Destination.objects.all()  # Fetch all destinations

    # Fetch all images and group them by destination
    destination_images = {
        destination.id: [{"image": image.image.url} for image in destination.images.all()]
        for destination in destinations
    }

    return render(request, 'main/gallery.html', {
        'popular_destinations': popular_destinations,
        'destinations': destinations,
        'destination_images': destination_images,  # Pass images as a serializable dictionary
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(**form.cleaned_data)

            # Add a success message
            messages.success(request, f'Thank you {request.user.username if request.user.is_authenticated else "for your message!"} We will get back to you soon.')

            return redirect('main:contact')  # Redirect after submission
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

@login_required
def upload_image(request, id):
    if request.method == "POST" and request.FILES.get("image"):
        destination = get_object_or_404(Destination, id=id)
        uploaded_image = Image(destination=destination, image=request.FILES["image"], uploaded_by=request.user)
        uploaded_image.save()
        return JsonResponse({"success": True, "image_url": uploaded_image.image.url})

    return JsonResponse({"success": False, "error": "Invalid request"})

def destination_detail(request, id):
    destination = get_object_or_404(Destination, id=id)
    images = destination.images.all()
    views_360 = destination.views_360.all()
    is_bookmarked = destination.bookmarked_by.filter(id=request.user.id).exists()
    
    # Fetch reviews related to the destination
    reviews = destination.reviews.all().order_by('-created_at')
    
    # Check if the user is subscribed
    # is_subscribed = request.user.is_subscribed() if request.user.is_authenticated else False
    
    return render(request, 'main/destination_detail.html', {
        'id': id,
        'destination': destination,
        'images': images,
        'views_360': views_360,
        'is_bookmarked': is_bookmarked,
        'reviews': reviews,
        # 'is_subscribed': is_subscribed,  # Add this line
    })


@login_required
def bookmarks(request):
    # Assuming you have a ManyToManyField 'bookmarked_by' in your Destination model
    bookmarked_destinations = Destination.objects.filter(bookmarked_by=request.user)
    return render(request, 'main/bookmarks.html', {'bookmarked_destinations': bookmarked_destinations})

@login_required
def toggle_bookmark(request, id):
    destination = get_object_or_404(Destination, id=id)
    if destination.bookmarked_by.filter(id=request.user.id).exists():
        # If the destination is already bookmarked, remove it
        destination.bookmarked_by.remove(request.user)
        messages.success(request, 'Destination removed from bookmarks.')
        bookmarked = False
    else:
        # If the destination is not bookmarked, add it
        destination.bookmarked_by.add(request.user)
        messages.success(request, 'Destination added to bookmarks.')
        bookmarked = True
    
    # Return a JSON response for AJAX requests
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'bookmarked': bookmarked})
    
    return redirect('main:bookmarks')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Bookmark
from .forms import BookmarkForm

# @login_required
# def add_bookmark(request):
#     if request.method == 'POST':
#         form = BookmarkForm(request.POST)
#         if form.is_valid():
#             bookmark = form.save(commit=False)
#             bookmark.user = request.user
#             bookmark.save()
#             return redirect('bookmark_list')  # Redirect to the list of bookmarks
#     else:
#         form = BookmarkForm()
#     return render(request, 'main/add_bookmark.html', {'form': form})

# @login_required
# def bookmark_list(request):
#     bookmarks = Bookmark.objects.filter(user=request.user)
#     return render(request, 'main/bookmark_list.html', {'bookmarks': bookmarks})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Destination, Review
from .forms import ReviewForm

@login_required(login_url='AUTH:login')
def submit_review(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.profile = request.user.profile
            review.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method.'})