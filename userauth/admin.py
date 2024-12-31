from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', 'email', 'phone', 'role', 'is_active', 'date_joined')  
    list_filter = ('role', 'is_staff', 'is_active', 'date_joined')  
    search_fields = ('username', 'email', 'phone')  
    ordering = ('-date_joined',)  


    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully activated {count} user(s).")
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Successfully deactivated {count} user(s).")
    deactivate_users.short_description = "Deactivate selected users"

admin.site.register(CustomUser, CustomUserAdmin)
