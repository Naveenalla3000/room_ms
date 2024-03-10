from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserProfileView,UserChagePasswordView,SendPasswordResetEmailView,UserPasswordResetView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register_drf'),
    path('login/', UserLoginView.as_view(), name='login_drf'),
    path('profile/', UserProfileView.as_view(), name='profile_drf'),
    path('changePassword/', UserChagePasswordView.as_view(), name='changePassword_drf'),
    path('send_reset_password_email/',SendPasswordResetEmailView.as_view(),name='send_reset_password-email_drf'),
    path('reset_password/<uidb64>/<token>/',UserPasswordResetView.as_view(), name='reset_password_drf'),
    path('logout/', views.logout, name='logout_drf'),
]