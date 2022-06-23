from .models import FaceDetected, UploadedImage
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class FaceDetectedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FaceDetected
        fields = ['Gender', 'StartX', 'StartY', 'EndX', 'EndY']


# Serializers define the API representation.
class UploadedImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['ImageFile', 'Gender', 'Confidence']