
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('account_test.urls')),
    path('accounts/', include('allauth.urls')),
    path('image_crete/',include('image_socal.urls')),

]
