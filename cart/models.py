from django.db import models
from django.conf import settings
from display.models import Product
from django.utils import timezone
from django.core.exceptions import ValidationError


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    



class ProductSales(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='sales_data')
    sales_count = models.PositiveIntegerField(default=0)  # Total products sold
    return_count = models.PositiveIntegerField(default=0)  # Total products returned
    

    def __str__(self):
        return f"{self.product.name} - Sales: {self.sales_count}, Returns: {self.return_count}"
    
    def save(self, *args, **kwargs):
        if self.sales_count < 0:
            raise ValidationError("Sales count cannot be negative.")
        super().save(*args, **kwargs)


class OrderDone(models.Model):
    order_id = models.CharField(max_length=20, unique=True , editable=False)
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
    

    def save(self, *args, **kwargs):
        if not self.order_id:
            today = timezone.now().strftime('%Y%m%d')
            count_today = OrderDone.objects.filter(created_at__date=timezone.now().date()).count()
            self.order_id = f'ORD{today}-{count_today + 1:03d}'
        super().save(*args, **kwargs)

