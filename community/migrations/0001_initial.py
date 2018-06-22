# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-06-22 05:29
from __future__ import unicode_literals

import community.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CommunityPostModel',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_content', models.TextField(default='내용이 없습니다', max_length=5000)),
                ('post_title', models.CharField(default='새 게시글', max_length=200)),
                ('is_visible', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoticePostModel',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_visible', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('post_title', models.CharField(default='새 공지사항', max_length=200)),
                ('post_content', models.TextField(default='내용이 없습니다')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCouncilModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', max_length=1000)),
                ('image', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=community.models.logo_file_path_generator)),
                ('main_contact', models.CharField(max_length=100)),
                ('sub_contact', models.CharField(max_length=100)),
                ('url', models.URLField(default='#')),
            ],
        ),
        migrations.CreateModel(
            name='StudyClubModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(default='', max_length=1000)),
                ('image', imagekit.models.fields.ProcessedImageField(default=None, null=True, upload_to=community.models.logo_file_path_generator)),
                ('main_contact', models.CharField(default='', max_length=100)),
                ('sub_contact', models.CharField(default='', max_length=100)),
                ('url', models.URLField(default='#')),
            ],
        ),
    ]