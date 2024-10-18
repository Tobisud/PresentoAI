from django.db import models
import uuid

class Presento(models.Model):
    title = models.CharField(max_length=255)
    pptx_file = models.FileField(upload_to='presento/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    process_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=50, default='pending')
    model_choice=models.IntegerField(default=1)
    process_percentage=models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    def __str__(self):
        return self.title
