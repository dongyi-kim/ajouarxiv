from django.contrib import admin
from community.models import *

# Register your models here.


class NoticePostModelAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user', 'post_title', 'is_visible', 'created_date', 'updated_date')
    search_fields = ('post_title', 'post_content')


admin.site.register(NoticePostModel, NoticePostModelAdmin)


class CommunityPostModelAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'user', 'post_title', 'is_visible', 'created_date', 'updated_date')
    search_fields = ('post_title', 'post_content')


admin.site.register(CommunityPostModel, CommunityPostModelAdmin)


class StudyClubModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_contact', 'sub_contact', 'url')
    search_fields = ('name', 'description', 'main_contact', 'sub_contact')

admin.site.register(StudyClubModel, StudyClubModelAdmin)


class StudentCouncilModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'main_contact', 'sub_contact', 'url')
    search_fields = ('name', 'description', 'main_contact', 'sub_contact')

admin.site.register(StudentCouncilModel, StudentCouncilModelAdmin)