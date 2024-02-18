from django.urls import path, include
from .views import image_create,image_detail,like_post_ajax,list_image

urlpatterns = [
    path('image_list/', list_image, name='list'),

    path('create/',image_create, name = 'image_create'),
    path('image_detail/<slug:slug>/<int:pk>/',image_detail, name = 'image_detail'),
    path('like/',like_post_ajax, name = 'like'),
    # path('users_list/',)


]
