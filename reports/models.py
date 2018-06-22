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

import time

class Report(models.Model):
    user        = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False)
    report_id   = models.AutoField(primary_key=True)
    is_public   = models.BooleanField(default=False)
    is_accessible= models.BooleanField(default=False)
    # is_file     = models.BooleanField(default=False, null=False, blank=False)
    # file_url    = models.URLField
    authors     = models.CharField(blank=True, null=False, max_length=100)

    title       = models.CharField(blank=False, null=False, max_length=100)
    # title_eng   = models.CharField(blank=False, null=False)

    abstract    = models.TextField(blank=True, null=False, default='')
    abstract_eng= models.TextField(blank=True, null=False, default='')

    created_date  = models.DateTimeField(auto_now_add=True)
    updated_date  = models.DateTimeField(auto_now=True)

    def set_public(self):
        self.is_public = True
        self.is_accessible = False
        self.save()

    def set_accessible(self):
        self.is_public = False
        self.is_accessible = True
        self.save()

    def set_private(self):
        self.is_public = False
        self.is_accessible = False
        self.save()

    def update(self):
        self.updated_date = timezone.now()
        authors_text = self.authors
        self.authors = ', '.join([author.strip() for author in authors_text.split(',')])
        self.save()

    def __str__(self):
        return "%s - %s (%s)" % (self.title, self.authors, self.user.email)


def report_file_path_generator(instance, filename):
    splited = filename.split('.')
    splited[-1] = time.strftime("%Y%m%d%H%M%S") + '.PDF'
    new_name = '.'.join(splited)
    id = str(instance.report.report_id)
    return 'reports/%s/%s/%s' %(instance.user.username, id,new_name)

@deconstructible
class ReportFileValidator(object):
    allowed_extensions = ['pdf']
    allowed_mime_types = ['application/pdf']
    minimum_file_size  = 10 # 10 Byte
    maximum_file_size =  30 * 1024 * 1024 #30 MB

    def __call__(self, file):
        if file.size < self.minimum_file_size:
            raise ValidationError("너무 작은 파일입니다.")

        if file.size > self.maximum_file_size:
            raise ValidationError("파일 크기는 30MB를 초과할 수 없습니다.")

        ext = os.path.splitext(file.name)[1][1:].lower()
        mimetype = mimetypes.guess_type(file.name)[0]
        if ext not in self.allowed_extensions or mimetype not in self.allowed_mime_types:
            raise ValidationError("PDF 파일만 업로드할 수 있습니다.")


class ReportFile(models.Model):
    report_file_id  = models.AutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    report          = models.ForeignKey(Report, on_delete=models.CASCADE, null=True)
    created_date    = models.DateTimeField(auto_now_add=True)
    commit_message  = models.CharField(blank=True, null=False, default='', max_length=1000)
    enabled         = models.BooleanField(default=False)
    filename        = models.CharField(default='file.pdf', max_length=200)
    file            = models.FileField(
        null=False,
        upload_to=report_file_path_generator,
        validators=[ReportFileValidator()]
    )

    def enable(self):
        ReportFile.objects.filter(report=self.report).update(enabled=False)
        self.enabled=True
        self.save()

#
# class ReportContent(models.Model):
#     report = models.ForeignKey(Report, on_delete=models.DO_NOTHING, unique=True, null=False, blank=False)
#     content_id = models.AutoField(primary_key=True)

