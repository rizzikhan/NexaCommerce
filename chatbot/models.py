from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='uploads/')
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
