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


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        return HttpResponse(status=404)


class LoginApiView(View):
    def get(self, request):
        return HttpResponse(status=404)

    def post(self, request):
        form = LoginForm(request.POST)
        username = request.POST['username']

        # 이메일 주소로 로그인 시도를 한 경우도 처리해줍니다.
        if User.objects.filter(email=username).exists():
            username = User.objects.get(email=username).username

        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


class LogoutView(View):

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('index')

    def post(self, request):
        return HttpResponse(status=404)


class RegisterView(View):
    def get(self, request):
        verification_id, hashcode = request.GET.get('verification_id'), request.GET.get('hashcode')
        verification = get_object_or_404(
            EmailVerification,
            verification_id=verification_id,
            hashcode=hashcode,
            expired_date__gte=timezone.now()
        )
        if User.objects.filter(email=verification.email).exists():
            return render(request, 'fail.html', {
                'title': '이미 가입되어 있습니다',
                'message': '이미 해당 아이디로 가입이 되어 있습니다!'
            })

        email = verification.email
        # 입력한 이메일의 호스트부를 계정으로 사용
        username = email.split("@")[0]

        return render(request, 'accounts/register.html', {
            'email': email, 'username': username,
            'verification_id': verification_id,
            'hashcode': hashcode,
        })

    def post(self, request):
        return HttpResponse(status=404)


class RegisterApiView(View):
    def get(self, request):
        return HttpResponse(status=404)

    def post(self, request):
        verification_id, hashcode = request.POST.get('verification_id'), request.POST.get('hashcode')

        # 이미 만료 되었거나, 존재하지 않는 이메일 인증 정보로 접근한 경우
        if not EmailVerification.objects.filter(
                verification_id=verification_id,
                hashcode=hashcode,
                expired_date__gte=timezone.now()
        ).exists():
            return HttpResponse(status=404)

        # 회원 가입을 요청한 경우
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            data = user_form.cleaned_data

            # 새 유저 객체 생성
            new_user = User.objects.create_user(
                username=data['username'],
                password=data['password1'],
                email=data['email']
            )

            print(new_user.profile)

            profile_form = ProfileUpdateForm(request.POST, instance=new_user.profile)
            profile_form.save()

            # 같은 이메일로 진행 된 기존의 모든 인증 요청을 만료시킨다
            EmailVerification.objects.get(verification_id=verification_id).expire()

            return HttpResponse(status=200)
        else:
            return HttpResponse(content=user_form.errors.as_json(), content_type="application/json", status=400)


class EmailVerificationView(View):
    def get(self, request):
        return render(request, 'accounts/email_verification.html')

    def post(self, request):
        return HttpResponse(status=404)


class EmailVerificationDoneView(View):
    def get(self, request):
        return render(request, 'done.html', {})

    def post(self, request):
        return HttpResponse(status=404)


class EmailVerificationApiView(View):
    def get(self, request):
        return HttpResponse(status=404)

    def post(self, request):
        # 사용자가 새로운 이메일 인증을 요청한 경우
        form = EmailVerificationCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if EmailVerification.objects.filter(email=email).exists():
                for ver in EmailVerification.objects.filter(email=email):
                    ver.expire()

            # 인증 정보를 생성하고 저장
            verification_request = form.save(commit=False)
            verification_request.request()

            # 유저에게 메일을 통한 가입 진행 요청
            send_mail(subject='1인1기1작 회원가입을 위한 이메일 인증 메일입니다!',
                      message='아래의 URL을 통해 회원 가입을 진행해주세요!' + '\n' + verification_request.get_url(),
                      from_email=settings.EMAIL_DISPLAYED_NAME,
                      recipient_list=[verification_request.email],
                      fail_silently=True)

            return HttpResponse(status=200)
        else:
            return HttpResponse(content=form.errors.as_json(), content_type="application/json", status=400)
