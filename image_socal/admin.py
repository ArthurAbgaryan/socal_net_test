from django.contrib import admin
from .models import Image

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title','slug','image','date_created']
    list_filter = ['date_created']

# Register your models here.
