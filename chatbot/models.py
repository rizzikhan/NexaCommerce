from django.db import models
from .utils import process_pdf
from django.conf import settings

class Document(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='uploads/')
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.processed:
            process_pdf(self.pdf_file.path)
            self.processed = True
            self.save()



class ChatHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="chat_histories"
    )
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"Chat with {user_display} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
