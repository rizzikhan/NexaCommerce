

from django.contrib import admin
from .models import EmailOTP

@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at')  
    list_filter = ('created_at',)  
    search_fields = ('email',)  
    ordering = ('-created_at',)  
