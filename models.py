from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import json
import numpy as np

class UploadedFile(models.Model):
    FILE_CATEGORIES = [
        ('files', 'Documents & Files'),
        ('videos', 'Videos & Movies'),
        ('audio', 'Music & Audio'),
        ('general', 'General Files'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    original_name = models.CharField(max_length=255, null=True)
    saved_name = models.CharField(max_length=255, null=True)
    file_path = models.CharField(max_length=500, null=True)
    file_size = models.BigIntegerField(null=True)
    category = models.CharField(max_length=20, choices=FILE_CATEGORIES, default='general')
    uploaded_at = models.DateTimeField(default=timezone.now, null=True)
    encrypted_file = models.CharField(max_length=500, null=True)
    otp = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'uploaded_files'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.original_name} ({self.user.username})"
    
    @property
    def file_url(self):
        """Return the URL to access the file"""
        from django.conf import settings
        return f"{settings.MEDIA_URL}{self.file_path}"
    
    @property
    def formatted_size(self):
        """Return human readable file size"""
        if self.file_size == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = self.file_size
        while size >= 1024 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        return f"{size:.2f} {size_names[i]}"
    
    
