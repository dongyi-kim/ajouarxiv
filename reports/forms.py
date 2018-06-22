from django.contrib.auth.models import User
from reports.models import Report, ReportFile
from django import forms


#
#
# class EmailVerificationCreationForm(forms.ModelForm):
#     class Meta:
#         model = EmailVerification
#         fields = ["email"]
#
#     def clean(self):
#         cleaned_data = super(EmailVerificationCreationForm, self).clean()
#         email = cleaned_data.get('email')
#         if not email or '@' not in email or len(email) <= 5:
#             raise forms.ValidationError("올바른 이메일 주소를 입력해주세요.")
#
#         username, domain = email.split('@')
#
#         if User.objects.filter(username=username).exists():
#             raise forms.ValidationError("이미 가입된 이메일 주소입니다.")
#
#         if domain not in settings.ALLOWED_EMAIL_DOMAIN:
#             raise forms.ValidationError("아주대학교 이메일 주소를 사용해주세요.")
#
#
#


class ReportModifyForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["title", 'abstract', 'abstract_eng', 'authors', 'is_accessible', 'is_public']


class ReportFileUploadForm(forms.ModelForm):
    class Meta:
        model = ReportFile
        fields = ['file', 'commit_message']
