from django.urls import path, include
from .views import main,register, edit_profile
from django.contrib.auth.views import LoginView,PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView

urlpatterns = [
    path('account_test/',main, name = 'main'),
    path('login/',LoginView.as_view(), name = 'login' ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/',PasswordChangeView.as_view(),name = 'password_change'),
    path('change_password_done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('reset_done/',PasswordResetDoneView.as_view(),name = 'password_reset_done'),
    path('password_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset_confim_done/',PasswordResetCompleteView.as_view(),name = 'password_reset_complete'),
    path('register_profile/',register, name = 'register'),
    path('edit_profile/',edit_profile, name = 'edit_profile'),

]
