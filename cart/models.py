from django.db import models
from django.conf import settings
from display.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class OrderDone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.JSONField()  
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    intent = models.CharField(max_length=255, null=True, blank=True)
    refund_status = models.CharField(max_length=50, default="Not Refunded")  
    is_refunded = models.BooleanField(default=False) 

    def __str__(self):
        return f"Order {self.id} - User: {self.user.username}"

