from django.contrib import admin
from .models import Destination, Contact, Image, View360, Review

class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'popular', 'category')
    search_fields = ('name', 'state', 'category')
    list_filter = ('name','state', 'popular', 'category')

admin.site.register(Destination, DestinationAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter = ('name','email')
admin.site.register(Contact, ContactAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('image', 'destination')
    list_filter = ('image','destination')
admin.site.register(Image, ImageAdmin)

# class View360Admin(admin.ModelAdmin):
#     list_display = ('destination',)
#     list_filter = ('destination',)
admin.site.register(View360)

from django.contrib import admin


from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Destination, Image
# from .forms import MultipleImageUploadForm

# class ImageAdmin(admin.ModelAdmin):
#     form = MultipleImageUploadForm
#     list_display = ['destination', 'image_preview']

#     def save_model(self, request, obj, form, change):
#         """Custom save method to handle multiple images"""
#         files = request.FILES.getlist('images')
#         if files:
#             for file in files:
#                 Image.objects.create(destination=obj.destination, image=file)
#         else:
#             super().save_model(request, obj, form, change)

#     def image_preview(self, obj):
#         return format_html('<img src="{}" width="50" height="50"/>'.format(obj.image.url)) if obj.image else "-"

#     image_preview.short_description = 'Preview'

# admin.site.register(Destination)
# admin.site.register(Image, ImageAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'rating', 'created_at')
    list_filter = ('user', 'destination', 'rating', 'created_at')
    search_fields = ('user__username', 'destination__name')    

admin.site.register(Review, ReviewAdmin)