from django import forms


class ImageUploadForm(forms.Form):
    ImageFile = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/*'}))
