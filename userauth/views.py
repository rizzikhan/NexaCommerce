from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser 
from .forms import *
from EMAILapp.utils import send_otp_email, verify_email_otp
from SMSapp.twilio_otp import send_otp
from django.urls import reverse
from django.contrib.auth import authenticate, login ,logout
from django_ratelimit.decorators import ratelimit



def signup_view(request):
    if request.method == 'POST':
        print("POST data:", request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            phone = form.cleaned_data['phone']
            role = form.cleaned_data['role']
    
            print(f"role selected: {role}")
            print(f"username selected: {username}")

            if CustomUser.objects.filter(email=email).exists():
                return render(request, 'userauth/signup.html', {'form': form, 'error': 'Email is already registered.'})

            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'userauth/signup.html', {'form': form, 'error': 'Username is already taken.'})

            if send_otp_email(email):

                user = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    phone=phone,
                    role=role,
                    is_active=False  
                )
                request.session['signup_data'] = {
                    'email': email,
                    'username': username,
                    'phone': phone,
                    'role': role,
                    'password': password
                }

                print(f"Signup data saved in session: {request.session['signup_data']}")
                return redirect('EMAILapp:verify_email_otp')

            return render(request, 'userauth/signup.html', {'form': form, 'error': 'Failed to send OTP.'})

        return render(request, 'userauth/signup.html', {'form': form, 'errors': form.errors})

    return render(request, 'userauth/signup.html', {'form': CustomUserCreationForm()})


@ratelimit(key='ip', rate='5/m', block=True)
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        print("We are in login_view")

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            print("in try block ")
            user = CustomUser.objects.get(email=email)
            print(user)
        except CustomUser.DoesNotExist:
            print("in except block ")
            return render(request, 'userauth/login.html', {'error': 'Invalid email or password'})

        print("before checking isactive block ")
        if not user.is_active:
            print("user is inactive snding otp ")
            if send_otp_email(email):
                print(" otp is true  ")

                request.session['otp_verification'] = {
                    'email': email
                }
                return redirect('EMAILapp:verify_email_otp')
            else:
                return render(request, 'userauth/login.html', {'error': 'Failed to send OTP. Please try again.'})

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            request.session['refresh_token'] = str(refresh)
            request.session['access_token'] = str(refresh.access_token)

            print(f"Access Token: {access_token}")
            print(f"Refresh Token: {refresh}")

            return redirect('display:display')
        else:
            return render(request, 'userauth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'userauth/login.html')

@ratelimit(key='ip', rate='5/m', block=True)
def reset_password_view(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']

            try:
                request.session['reset_email'] = email
                request.session['reset_phone'] = phone
                print("Got data from form and saved email and phone in session.")
                reset_email = request.session.get('reset_email')
                reset_phone = request.session.get('reset_phone')
                print(reset_email, reset_phone)
                print("Now redirecting to userauth/otp_method_selection")
                return redirect('userauth:otp_method_selection')  
            except CustomUser.DoesNotExist:
                return render(
                    request, 
                    'userauth/reset_password.html', 
                    {'form': form, 'error': 'No user found with the provided email and phone number.'}
                )

        return render(request, 'userauth/reset_password.html', {'form': form, 'errors': form.errors})

    return render(request, 'userauth/reset_password.html', {'form': ResetPasswordForm()})


def otp_method_selection_view(request):
    if request.method == 'POST':
        method = request.POST.get('otp_method')
        email = request.session.get('reset_email')
        phone = request.session.get('reset_phone')
        print("got method of selection and got email and phone from sessions")

        if method == 'email' and send_otp_email(email):

            return redirect('EMAILapp:verify_forgot_otp')
        
        elif method == 'sms' and send_otp(phone):
            return redirect(reverse('SMSapp:verify_otp', kwargs={'phone_number': phone}))
        
        return render(request, 'userauth/otp_method_selection.html', {'error': 'Failed to send OTP.'})

    return render(request, 'userauth/otp_method_selection.html')


def verify_otp_view(request):
    email = request.session.get('reset_email')  
    print("now getting data of session ")
    print(email)
    print("now we are in verify otp view for reset password ")
    if not email:
        print("no email in session ")
        return redirect('userauth:reset_password')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            print("we got otp from user using form ")
            if verify_email_otp(email, otp):
                request.session['otp_verified'] = True
                print("redirecting to new password page")
                return redirect('userauth:set_new_password')  
            print("verify_email_otp result is false so redirecting to verify otp again ")
            return render(request, 'userauth/verify_otp.html', {
                'form': form,
                'error': 'Invalid OTP. Please try again.'
            })

    return render(request, 'userauth/verify_otp.html', {'form': OTPForm()})

def set_new_password_view(request):
    email = request.session.get('reset_email')  
    otp_verified = request.session.get('otp_verified')  
    print("getting data from session for email and otp_verified  for sms otp ")
    print(email , otp_verified)
    if not email or not otp_verified:
        return redirect('userauth:reset_password')

    if request.method == 'POST':
        form = NewPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            if new_password != confirm_password:
                return render(request, 'userauth/set_new_password.html', {
                    'form': form,
                    'error': 'Passwords do not match.'
                })

            try:
                user = CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                del request.session['reset_email']
                del request.session['otp_verified']

                return redirect('userauth:login') 
            except CustomUser.DoesNotExist:
                return redirect('userauth:reset_password')

    return render(request, 'userauth/set_new_password.html', {'form': NewPasswordForm()})

def logout_view(request):
     logout(request) 
     return redirect('display:display')  

