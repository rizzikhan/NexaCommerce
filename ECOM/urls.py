
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),

    path("" , include('display.urls')), #dashboard

    path('userauth/', include('userauth.urls')),  #for user login and signup

    
    path('email-otp/', include('EMAILapp.urls')), #for email verification

    path('sms/', include('SMSapp.urls')),  #for sms verification

    path('api/cart/', include('cart.urls')), #for cart 

    path('chatbot/', include('chatbot.urls')), #for bot 

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)