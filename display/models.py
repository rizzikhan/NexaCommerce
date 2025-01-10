from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from django.urls import reverse
import bleach  


def validate_positive(value):
    if value <= 0:
        raise ValidationError("Value must be greater than zero.")


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class CarouselImage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)  
    image = CloudinaryField('image')  
    description = models.TextField(blank=True, null=True)  
    order = models.PositiveIntegerField(default=0)  
    is_active = models.BooleanField(default=True)  

    class Meta:
        ordering = ['order'] 

    def __str__(self):
        return self.title or f"Carousel Image {self.pk}"
    
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2 , validators=[validate_positive])
    stock = models.PositiveIntegerField(default=0 , validators=[validate_positive])
    image = CloudinaryField('product_image', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True)

    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="merchant_products"
    )
    created_at = models.DateTimeField(auto_now_add=True , null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('display:detailedpage', args=[str(self.id)])
    
    def save(self, *args, **kwargs):
        allowed_tags = ['b', 'i', 'u', 'strong', 'em', 'p', 'ul', 'li', 'ol', 'a', 'br']
        allowed_attributes = {'a': ['href', 'title', 'target']}

        if self.description:
            self.description = bleach.clean(self.description, tags=allowed_tags, attributes=allowed_attributes, strip=True)

        super().save(*args, **kwargs)
    





class Watchlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField() 
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating})"
    