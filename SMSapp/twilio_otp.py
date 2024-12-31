from twilio.rest import Client
from django.conf import settings


#called when selection 
def send_otp(phone_number):
    print("now we are sending sms otp for reset password ")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        verification = client.verify \
            .services(settings.TWILIO_VERIFY_SERVICE_SID) \
            .verifications \
            .create(to=phone_number, channel='sms')
        print("SMS OTP SENT SUCCESSFULLY")
        return verification.status  
    except Exception as e:
        print(f"Twilio Error: {str(e)}")  
        return str(e)

def verify_otp(phone_number, code):
    print("now we are in to verify otp by verification_checks")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    print("twilio authenticaiton successful ")
    try:
        verification_check = client.verify \
            .services(settings.TWILIO_VERIFY_SERVICE_SID) \
            .verification_checks \
            .create(to=phone_number, code=code)
        print( "approve or not ?" )
        print(verification_check.status)
        return verification_check.status  
    except Exception as e:
        return str(e)
