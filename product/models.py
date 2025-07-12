from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    uploader_id = models.CharField(max_length=128)  # Firebase UID
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    condition = models.CharField(max_length=100)
    image_url=models.URLField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title