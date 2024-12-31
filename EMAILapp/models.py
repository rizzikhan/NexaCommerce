from django.db import models
from django.utils.timezone import now

class EmailOTP(models.Model):
    email = models.EmailField(unique=True)  
    otp = models.IntegerField() 
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.email} - {self.otp}"
