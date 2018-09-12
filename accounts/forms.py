# -*- coding: utf-8 -*-
from django import forms
from ajouarxiv import settings

from accounts.models import Profile, EmailVerification
from django.contrib.auth.models import User

import re


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50)
    student_id = forms.CharField(max_length=9)
    email = forms.EmailField(max_length=100)
    name_kor = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    # name_eng    = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        student_id = cleaned_data.get('student_id')
        email = cleaned_data.get('email')
        name_kor = cleaned_data.get('name_kor')
        # name_eng = cleaned_data.get('name_eng')
        password = cleaned_data.get('password1')
        password_confirm = cleaned_data.get('password2')

        if not email or '@' not in email or len(email) <= 5:
            raise forms.ValidationError("올바른 이메일 주소를 입력해주세요.")

        username, domain = email.split('@')

        if not username or User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 가입된 아이디입니다.")

        if domain not in settings.ALLOWED_EMAIL_DOMAIN:
            raise forms.ValidationError("올바르지 않은 이메일 도메인입니다.")

        if not name_kor or not re.compile('^[가-힣]{2,20}$').match(name_kor):
            raise forms.ValidationError("한글 이름은 10글자 이하의 한글이어야 합니다.")
        #
        # if not name_eng or not re.compile('^(?=.*[a-z ])(?=.{3,50})$').match(name_eng):
        #     raise forms.ValidationError("영문 이름은 공백과 알파벳 소문자로 이루어진 3~50글자여야 합니다.")

        if not student_id or not re.compile("^[0-9]{9,9}$").match(student_id):
            raise forms.ValidationError("올바른 9자리 학번(사번)을 입력해주세요.")

        if password != password_confirm:
            raise forms.ValidationError("두 비밀번호가 일치하지 않습니다.")

        if not re.compile('^[a-zA-Z0-9!@#$%^&*]{8,30}$').match(password):
            raise forms.ValidationError("비밀번호는 8~30글자 사이어야 하며,<br/>대/소문자, 숫자, 특수기호(!@#$%%^&*)만 사용 가능합니다.")


class EmailVerificationCreationForm(forms.ModelForm):
    class Meta:
        model = EmailVerification
        fields = ["email"]

    def clean(self):
        cleaned_data = super(EmailVerificationCreationForm, self).clean()
        email = cleaned_data.get('email')
        if not email or '@' not in email or len(email) <= 5:
            raise forms.ValidationError("올바른 이메일 주소를 입력해주세요.")

        username, domain = email.split('@')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 가입된 이메일 주소입니다.")

        if domain not in settings.ALLOWED_EMAIL_DOMAIN:
            raise forms.ValidationError("아주대학교 이메일 주소를 사용해주세요.")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name_kor', 'student_id']

    def clean(self):
        cleaned_data = super(ProfileUpdateForm, self).clean()
        student_id = cleaned_data.get('student_id')
        name_kor = cleaned_data.get('name_kor')

        if not name_kor or not re.compile('^[가-힣]{2,20}$').match(name_kor):
            raise forms.ValidationError("한글 이름은 10글자 이하의 한글이어야 합니다.")

        if not student_id or not re.compile("^[0-9]{9,9}$").match(student_id):
            raise forms.ValidationError("올바른 9자리 학번(사번)을 입력해주세요.")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class PasswordChangeForm(forms.ModelForm):
    pass