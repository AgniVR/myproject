from django.shortcuts import render

# Create your views here.
import random

from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .models import User

def generate_otp():
    otp = random.randint(1000, 9999)  # Generate a random 4-digit OTP
    return str(otp)

def send_otp(email, otp):
    message = f"Your OTP is: {otp}"
    send_mail("OTP Verification", message, settings.DEFAULT_FROM_EMAIL, [email])

def validate_otp(email, otp):
    # Compare the provided OTP with the expected value
    expected_otp = "1234"  # Replace with your OTP generation logic or actual OTP value

    return otp == expected_otp

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')

        # Generate and send OTP
        otp = generate_otp()
        send_otp(email, otp)  # Implement OTP delivery logic

        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            phone_number=phone_number
        )

        # Set user as inactive until OTP verification
        user.is_active = False
        user.save()

        return JsonResponse({'message': 'User created successfully. Check your email for OTP.'})

    return render(request, 'signup.html')

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        # Validate OTP
        if validate_otp(email, otp):  # Implement OTP validation logic
            user = User.objects.get(email=email)
            user.is_active = True
            user.save()
            auth_login(request, user)
            return JsonResponse({'message': 'Logged in successfully.'})
        else:
            return JsonResponse({'message': 'Invalid OTP.'})

    return render(request, 'login.html')

def user_logout(request):
    auth_logout(request)
    return JsonResponse({'message': 'Logged out successfully.'})
