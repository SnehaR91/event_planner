# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/<int:user_id>/<str:token>/', verify_email, name='verify_email'),
    path('resend-verification/', resend_verification_email, name='resend_verification'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
