from django import forms
from django.contrib.auth.forms import  UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password



class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    email = forms.EmailField(required=True, label="Email")
    phone = forms.CharField(max_length=20, required=True, label="Phone")
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password",
        help_text="Your password must be at least 6 characters long and contain one uppercase letter, one lowercase letter, one digit, and one special character.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget = forms.Select(choices=CustomUser.ROLE_CHOICES)  

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "phone", "role"]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(e.messages)
        
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not any(char.isupper() for char in password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not any(char in '!@#$%^&*()_+' for char in password):
            raise forms.ValidationError("Password must contain at least one special character (!@#$%^&*).")
        
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password']) 
        if commit:
            user.save()
        return user



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError('Phone number must contain only digits.')
        return phone

class loginform(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)


class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

