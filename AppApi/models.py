from django.db import models


# Create your models here.
class UploadedImage(models.Model):
    ImageFile = models.ImageField(null=False, upload_to='image/')
    Gender = models.CharField(max_length=6, default='Male')
    Confidence = models.FloatField(default=0)

class FaceDetected(models.Model):
    Gender = models.CharField(max_length=6, default='Male')
    StartX = models.IntegerField(default=0)
    StartY = models.IntegerField(default=0)
    EndX = models.IntegerField(default=0)
    EndY = models.IntegerField(default=0)
    Image = models.ForeignKey('UploadedImage', unique=False, null=False, default=None, on_delete=models.CASCADE)

