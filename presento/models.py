from django.db import models
import uuid

class Presento(models.Model):
    title = models.CharField(max_length=255)
    pptx_file = models.FileField(upload_to='presento/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    process_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=50, default='pending')
    def __str__(self):
        return self.title
