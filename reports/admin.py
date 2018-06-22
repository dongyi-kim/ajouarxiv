from django.contrib import admin
from reports.models import Report, ReportFile


# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'title', 'user', 'authors', 'is_public', 'created_date', 'updated_date',)
    search_fields = ('report_id', 'title', 'authors', 'abstract', 'abstract_eng')


admin.site.register(Report, ReportAdmin)


class ReportFileAdmin(admin.ModelAdmin):
    list_display = ('report_file_id', 'user', 'report', 'enabled', 'commit_message', 'file', 'created_date',)
    search_fields = ('report_file_id', 'commit_message')


admin.site.register(ReportFile, ReportFileAdmin)
