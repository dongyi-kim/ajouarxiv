from django.contrib import admin
from accounts.models import Profile, EmailVerification


# Register your models here.


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('verification_id', 'email', 'created_date', 'expired_date', 'hashcode')
    search_fields = ('verification_id', 'email')


admin.site.register(EmailVerification, EmailVerificationAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'name_kor')
    search_fields = ('student_id', 'name_kor')


admin.site.register(Profile, ProfileAdmin)
