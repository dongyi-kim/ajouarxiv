# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import EmailVerificationCreationForm, RegisterForm, LoginForm, ProfileUpdateForm
from accounts.models import Profile, EmailVerification
# Create your views here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.views.generic import View, FormView
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ajouarxiv import settings
import json
from django.core import exceptions


class ProfileBasicInformationView(View):

    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'accounts/profile_update.html', {
            'user': request.user
        })

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=404)
