from django.shortcuts import render, redirect
from EMAILapp.utils import *
from django.contrib.auth.models import Group
from userauth.models import CustomUser
from .utils import verify_email_otp  
from django.contrib.auth import  login
from rest_framework_simplejwt.tokens import RefreshToken


# for signup email otp verificaion
def verify_email_otp_view(request):

    if request.method == 'POST':
        otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data')

        if not signup_data:
            return redirect('userauth:signup')

        email = signup_data.get('email')

        if not email:
            return redirect('userauth:signup')
        
        # in userauth/utils 
        if verify_email_otp(email, otp):
            try:
                user = CustomUser.objects.get(email=email)
                user.is_active = True  
                user.save()

                role = signup_data.get('role')
                if role:
                    try:
                        group = Group.objects.get(name=role)
                        user.groups.add(group)
                    except Group.DoesNotExist:
                        return render(request, 'EMAILapp/verify_email_otp.html', {
                            'error': f"Role '{role}' does not exist. Please contact support."
                        })

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                request.session['refresh_token'] = str(refresh)
                request.session['access_token'] = access_token

                print(f"Refresh token: {refresh}")
                print(f"Access token: {access_token}")

                login(request, user)
                del request.session['signup_data']  

                return redirect('display:display')

            except CustomUser.DoesNotExist:
                return render(request, 'EMAILapp/verify_email_otp.html', {
                    'error': 'User does not exist.'
                })
            except Exception as e:
                return render(request, 'EMAILapp/verify_email_otp.html', {
                    'error': f"Error activating user: {str(e)}"
                })

        return render(request, 'EMAILapp/verify_email_otp.html', {
            'error': 'Invalid OTP. Please try again.'
        })

    return render(request, 'EMAILapp/verify_email_otp.html')




#---------------------------------------------------------------------------------

def verify_email_otp_view_reset(request):
    if request.method == 'POST':
        print("now we are in verify_email_otp for Reset user")
        otp = request.POST.get('otp')
        email = request.session.get('email') 
        print("print sesstion data of reset data  ")
        print(email)
        if not email:
            print("email is empty that why go to signup means session data is no more ")
            return redirect('userauth:signup') 
        
    return redirect('userauth:verify_otp') 
