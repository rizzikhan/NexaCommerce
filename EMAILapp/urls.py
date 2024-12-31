from django.urls import path
from . import views

app_name = 'EMAILapp'

urlpatterns = [
    path('verify-otp/', views.verify_email_otp_view, name='verify_email_otp'),
    path('verify-reset-otp/', views.verify_email_otp_view_reset, name='verify_forgot_otp'),

]
