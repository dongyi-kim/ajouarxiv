# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible

import os
import mimetypes
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import time

# Django 3rd Party Modules
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit


def report_file_path_generator(instance, filename):
    return 'files/%s/%s' % (instance.user.username, filename)


@deconstructible
class FileResourceValidator(object):
    allowed_extensions = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'zip', 'gz', 'txt', 'hwp', 'doc', 'docx', 'xls',
                          'xlsx', 'xml', 'json', 'ppt', 'pptx', 'ai']
    allowed_mime_types = ['application/pdf']
    minimum_file_size = 10  # 10 Byte
    maximum_file_size = 30 * 1024 * 1024  # 30 MB

    def __call__(self, file):
        if file.size < self.minimum_file_size:
            raise ValidationError("너무 작은 파일입니다.")

        if file.size > self.maximum_file_size:
            raise ValidationError("파일 크기는 30MB를 초과할 수 없습니다.")

        ext = os.path.splitext(file.name)[1][1:].lower()
        mimetype = mimetypes.guess_type(file.name)[0]
        if ext not in self.allowed_extensions or mimetype not in self.allowed_mime_types:
            raise ValidationError("업로드할 수 없는 파일입니다.\n 가능한 파일 : " + str(self.allowed_extensions))


class FileResourceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    file_id = models.AutoField(primary_key=True)
    file = models.FileField(
        null=False,
        upload_to=report_file_path_generator,
        validators=[FileResourceValidator()]
    )


class ImageResourceModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    image_id = models.AutoField(primary_key=True)
    image = ProcessedImageField(null=False,
                                upload_to=report_file_path_generator,
                                processors=[ResizeToFit(1024, 1024, False)])
