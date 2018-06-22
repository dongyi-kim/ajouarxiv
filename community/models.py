from django.db import models

from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.


# Django 3rd Party Modules
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class CommunityPostModel(models.Model):
    post_id      = models.AutoField(primary_key=True)
    post_content = models.TextField(default='내용이 없습니다', null=False, max_length=5000)
    post_title   = models.CharField(default='새 게시글', null=False, max_length=200)
    user         = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    is_visible   = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class CommunityPostForm(ModelForm):
    class Meta:
        model = CommunityPostModel
        fields = ['post_content', 'post_title']



class NoticePostModel(models.Model):
    post_id      = models.AutoField(primary_key=True)
    user         = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    is_visible   = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    post_title   = models.CharField(default='새 공지사항', null=False, max_length=200)
    post_content = models.TextField(default='내용이 없습니다', null=False)


class NoticePostForm(ModelForm):
    class Meta:
        model = NoticePostModel
        fields = ['post_content', 'post_title']



def logo_file_path_generator(instance, filename):
    return 'images/logo/%s' % filename



class StudyClubModel(models.Model):
    name        = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(default='', max_length=1000)
    image = ProcessedImageField(null=True, default=None,
                                upload_to=logo_file_path_generator,
                                processors=[ResizeToFill(344, 344, False)])

    main_contact= models.CharField(null=False, blank=False, default='', max_length=100)
    sub_contact = models.CharField(null=False, blank=False, default='', max_length=100)
    url         = models.URLField(null=False, blank=False, default='#')


class StudentCouncilModel(models.Model):
    name        = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(default='', max_length=1000)
    image = ProcessedImageField(null=True, default=None,
                                upload_to=logo_file_path_generator,
                                processors=[ResizeToFill(344, 344, False)])

    main_contact= models.CharField(null=False, blank=False, max_length=100)
    sub_contact = models.CharField(null=False, blank=False, max_length=100)
    url         = models.URLField(null=False, blank=False, default='#')


