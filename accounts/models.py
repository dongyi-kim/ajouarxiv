from django.db import models
from django import forms
from django.utils import timezone
import hashlib
from django.shortcuts import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.


from urllib import parse
from ajouarxiv import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, default='학번없음')
    name_kor = models.CharField(max_length=20, default='이름없음')

    # name_eng    = models.CharField(max_length=50, default='Anonymous')

    def __str__(self):
        return "%s (%s, %s)" % (self.name_kor, self.student_id, self.user.email)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        print(profile)


post_save.connect(create_user_profile, sender=User)
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])



class EmailVerification(models.Model):
    verification_id = models.AutoField(primary_key=True)
    email = models.EmailField(null=False, blank=False)
    hashcode = models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    expired_date = models.DateTimeField(default=timezone.now)
    trash = models.CharField(max_length=256, null=True)

    def request(self):
        self.created_date = timezone.now()
        self.expired_date = timezone.now() + timezone.timedelta(hours=24)

        h = hashlib.sha256()
        h.update(str(self.verification_id).encode('utf-8'))
        h.update(self.email.encode('utf-8'))

        self.hashcode = h.hexdigest()
        self.save()

    def expire(self):
        self.expired_date = timezone.now()
        self.save()

    def get_url(self):
        host = '%s://%s' % (settings.BASE_PROTOCOL, settings.BASE_HOST)
        query = '?verification_id=%d&hashcode=%s' % (self.verification_id, self.hashcode)
        url = parse.urljoin(host, reverse('register'))
        url = parse.urljoin(url, query)
        return url


class PasswordChangeRequest(models.Model):
    user = models.ForeignKey(User)
    request_id = models.AutoField(primary_key=True)
    hashcode = models.CharField(max_length=256, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    expired_date = models.DateTimeField(default=timezone.now)

    def request(self):
        self.created_date = timezone.now()
        self.expired_date = timezone.now() + timezone.timedelta(hours=24)

        h = hashlib.sha256()
        h.update(str(self.request_id).encode('utf-8'))
        h.update(self.user.email.encode('utf-8'))

        self.hashcode = h.hexdigest()
        self.save()

    def expire(self):
        self.expired_date = timezone.now()
        self.save()

    def get_url(self):
        host = '%s://%s' % (settings.BASE_PROTOCOL, settings.BASE_HOST)
        query = '?request_id=%d&hashcode=%s' % (self.request_id, self.hashcode)
        url = parse.urljoin(host, reverse('profile_password_change'))
        url = parse.urljoin(url, query)
        return url
