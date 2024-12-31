from random import randint
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailOTP


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
        send_mail(subject, message, from_email, [email])
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
