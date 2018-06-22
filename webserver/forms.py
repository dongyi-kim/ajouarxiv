from django.forms import ModelForm
from webserver.models import ImageResourceModel


class ImageUploadForm(ModelForm):
    class Meta:
        model = ImageResourceModel
        fields = ['image']
