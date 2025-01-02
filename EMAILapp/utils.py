from random import randint
from django.conf import settings
from .models import EmailOTP
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime

def generate_otp():
    return randint(100000, 999999)


# for signup send otp 
def send_otp_email(email):
    print("Sending OTP via email...")
    otp = generate_otp()
    try:
        EmailOTP.objects.update_or_create(email=email, defaults={'otp': otp})
        subject = 'Your OTP for Verification'
        message = f'Your OTP is: {otp}'
        from_email = settings.EMAIL_HOST_USER
        to = [email]

        context = {
            'otp': otp,
            'email': email,
            'notice': 'Use the OTP below to complete your verification process.',
            'congratulations_message': 'Congratulations! You’re just one step away from accessing exclusive features.',
            'current_year': datetime.now().year

        }
        html_content = render_to_string('EMAILapp/otp_email.html', context)
        text_content = f"Congratulations! Your OTP is: {otp}. Please use it to complete your verification."

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        print("OTP email sent successfully.")
        return True
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

def verify_email_otp(email, otp):
    try:
        record = EmailOTP.objects.get(email=email)
        if str(record.otp) == str(otp):
            record.delete()
            print("OTP matched successfully.")
            return True
    except EmailOTP.DoesNotExist:
        print("OTP record not found.")
    return False
