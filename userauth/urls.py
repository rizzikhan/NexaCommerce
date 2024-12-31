from django.urls import path 

from . import views


app_name = "userauth"

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('otp-method-selection/', views.otp_method_selection_view, name='otp_method_selection'),  
    path('verify-otp/', views.verify_otp_view, name='verify_otp'), 
    path('set-new-password/', views.set_new_password_view, name='set_new_password'),  
    path('logout/', views.logout_view , name='logout'),

    
]