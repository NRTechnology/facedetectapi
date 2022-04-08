from django.urls import path

from .views import UploadImage

urlpatterns = [
    path('upload/', UploadImage.as_view(), name='UploadApi'),
]