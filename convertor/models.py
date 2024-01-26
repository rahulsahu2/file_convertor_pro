from django.db import models

# Create your models here.
class ReceiptFile(models.Model):
    """Model for storing receipt file"""
    file = models.FileField(upload_to='receipts/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    converted_csv = models.FileField(upload_to='receipts/converted_csv/', null=True, blank=True)
    

    def __str__(self):
        return self.file.name
    
