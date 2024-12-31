from django.contrib.auth.models import AbstractUser , Group, Permission
from django.db import models
from display.models import Product

class CustomUser(AbstractUser):
    watchlist_by = models.ManyToManyField(Product, blank=True, related_name='watchlisted_by')
    is_active = models.BooleanField(default=False)  
    ROLE_CHOICES = [
        ("normal", "Normal User"),
        ("merchant", "Merchant"),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default="normal"
    )
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"



    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",  
        blank=True,
    )