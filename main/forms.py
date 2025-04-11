from django import forms
from django.core.exceptions import ValidationError
import re

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your message here...'}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10,15}$', phone):
            raise ValidationError("Phone number must be between 10 and 15 digits.")
        return phone

from django import forms
from .models import Image
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Bookmark


# class MultipleImageUploadForm(forms.ModelForm):
#     images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=True)

#     class Meta:
#         model = Image
#         fields = ['destination', 'images']

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         files = self.files.getlist('images')

#         image_instances = []
#         for file in files:
#             image_instance = Image(destination=instance.destination, image=file)
#             image_instances.append(image_instance)

#         # Bulk create for efficiency
#         Image.objects.bulk_create(image_instances)
#         return instance

class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ['url', 'title', 'description']
        
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        # widgets = {
        #     'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Write your review...'}),
        #     'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        # }