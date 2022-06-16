from django.urls import path

from .views import UploadImage, HelloView

urlpatterns = [
    path('upload/', UploadImage.as_view(), name='UploadApi'),
    path('hello/', HelloView.as_view(), name='hello')
]