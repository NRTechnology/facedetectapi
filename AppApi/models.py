from django.db import models


# Create your models here.
class UploadedImage(models.Model):
    ImageFile = models.ImageField(null=False, upload_to='image/')
