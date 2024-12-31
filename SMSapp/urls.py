from django.urls import path
from . import views

app_name = 'SMSapp'  

urlpatterns = [
    path('verify-otp/<str:phone_number>/', views.verify_otp_view, name='verify_otp'),

]
