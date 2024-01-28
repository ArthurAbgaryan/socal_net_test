from django.urls import path, include
from .views import image_create

urlpatterns = [
    path('create/',image_create, name = 'image_create'),


]
