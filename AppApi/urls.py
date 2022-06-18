from django.urls import path

from .views import UploadImage, HelloView

urlpatterns = [
    path('v1/process/', UploadImage.as_view(), name='UploadApi'),
    path('hello/', HelloView.as_view(), name='hello')
]