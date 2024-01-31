from django.urls import path, include
from .views import image_create,image_detail,like_ajax

urlpatterns = [
    path('create/',image_create, name = 'image_create'),
    path('image_detail/<slug:slug>/<int:pk>/',image_detail, name = 'image_detail'),
    path('like/',like_ajax, name = 'like')


]
