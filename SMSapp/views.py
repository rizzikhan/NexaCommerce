from django.shortcuts import render, redirect
from .twilio_otp import verify_otp


def verify_otp_view(request, phone_number):
    print("we are in verfiy_otp_view for sms OTP")
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        print("this is otp recived from user ")
        print(otp_code)
        if otp_code:
            print("otpcode has some value so we got in and now verifying otp status")
            status = verify_otp(phone_number, otp_code)
            if status == 'approved':
                request.session['otp_verified'] = True
                print("staus is approved now redirect to set_new_password")
                return redirect('userauth:set_new_password')
            else:
                return render(request, 'SMSapp/verify_otp.html', {
                    'phone_number': phone_number,
                    'error': 'Invalid OTP. Please try again.',
                })

    return render(request, 'SMSapp/verify_otp.html', {'phone_number': phone_number})
