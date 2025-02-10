from django.shortcuts import render

# Create your views here.

# users/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import CustomUser
from .forms import RegistrationForm
from .signals import send_verification_email


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login before email verification
            user.save()
            messages.success(request, "Check your email to verify your account.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_email(request, user_id, token):
    user = get_object_or_404(CustomUser, pk=user_id)
    if default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True  # Activate user
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid verification link!")
        return redirect('register')

def resend_verification_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user and not user.is_verified:
            send_verification_email(user)
            messages.success(request, "Verification email sent!")
        else:
            messages.error(request, "User not found or already verified.")
    return render(request, 'users/resend_verification.html')


# users/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_verified:  # Check email verification
                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect('event_list')  # Redirect to events page
                else:
                    messages.error(request, "Email not verified! Please check your inbox.")
            else:
                messages.error(request, "Invalid email or password.")
    
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login')
