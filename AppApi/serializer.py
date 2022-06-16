from .models import FaceDetected
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class FaceDetectedSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FaceDetected
        fields = ['Gender', 'StartX', 'StartY', 'EndX', 'EndY']
