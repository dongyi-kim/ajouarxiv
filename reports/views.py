from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.db.models import Q
from urllib.parse import urlencode
from reports.models import Report, ReportFile
from accounts.models import Profile
from ajouarxiv import settings

from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator

import urllib.parse
import time

from reports.forms import ReportModifyForm, ReportFileUploadForm
import os


# Create your views here.


class ReportHomeView(View):
    def get(self, request):
        return render(request, 'reports/home.html', {})

    def post(self, request):
        return HttpResponseNotFound()


class ReportListView(ListView):
    model = Report
    template_name = 'reports/list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)

        filter = {}
        if self.request.GET.get('author'):
            filter['user'] = self.request.GET.get('author')

        if self.request.GET.get('title'):
            filter['title'] = self.request.GET.get('title')

        if self.request.GET.get('abstract'):
            filter['content'] = self.request.GET.get('abstract')

        context['filter'] = filter

        return context

    def get_queryset(self):
        queryset = Report.objects.filter(is_public=True)
        if self.request.GET.get('author'):
            pattern = self.request.GET.get('author')
            users = User.objects.filter(username__contains=pattern)
            profiels = Profile.objects.filter(name_kor__contains=pattern).values_list('user', flat=True)
            queryset = queryset.filter(Q(user__in=users) | Q(user__in=set(profiels)) | Q(authors__contains=pattern))

        if self.request.GET.get('title'):
            pattern = self.request.GET.get('title')
            queryset = queryset.filter(title__contains=pattern)

        if self.request.GET.get('abstract'):
            pattern = self.request.GET.get('abstract')
            queryset = queryset.filter(abstract__contains=pattern)

        return queryset.order_by('-created_date')


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/view.html'
    context_object_name = 'report'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object.is_public and self.object.user != request.user:
            raise Http404

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(ReportDetailView, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.object.user)
        context['report_url'] = urllib.parse.urljoin(settings.BASE_URL, 'p/%d/' % self.object.report_id)
        if ReportFile.objects.filter(report=self.object, enabled=True).exists():
            context['report_file'] = ReportFile.objects.get(report=self.object, enabled=True)
        return context


class ReportHelpView(View):
    def get(self, request):
        return render(request, 'reports/help.html', {})

    def post(self, request):
        raise Http404


@method_decorator(login_required, name='dispatch')
class ReportMyWritingsView(View):
    def get(self, request):
        queryset = Report.objects.filter(user=request.user)
        if self.request.GET.get('author'):
            pattern = self.request.GET.get('author')
            queryset = queryset.filter(authors__contains=pattern)

        if self.request.GET.get('title'):
            pattern = self.request.GET.get('title')
            queryset = queryset.filter(title__contains=pattern)

        if self.request.GET.get('abstract'):
            pattern = self.request.GET.get('abstract')
            queryset = queryset.filter(abstract__contains=pattern)
        queryset = queryset.order_by('-created_date')
        return render(request, 'reports/writings.html', {'object_list': queryset})

    def post(self, request):
        raise Http404


@method_decorator(login_required, name='dispatch')
class ReportInfoModifyView(View):

    def get(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        context = {
            'report': report,
            'user': request.user,
            'profile': get_object_or_404(Profile, user=request.user),
            'report_file_exists': ReportFile.objects.filter(report=report, enabled=True).exists()
        }

        return render(request, 'reports/modify_info.html', context)

    def post(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        form = ReportModifyForm(request.POST, instance=report)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            report.update()
        else:
            return HttpResponse(status=400)

        return HttpResponse(status=200)


@method_decorator(login_required, name='dispatch')
class ReportFileModifyView(View):

    def get(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        file_list = ReportFile.objects.filter(report=report).order_by('-report_file_id')
        context = {
            'file_list': file_list,
            'user': request.user,
            'profile': get_object_or_404(Profile, user=request.user),
            'report': report
        }

        return render(request, 'reports/modify_files.html', context)

    def post(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        report_file_id = request.POST['report_file_id']
        file = get_object_or_404(ReportFile, user=request.user, report=report, report_file_id=report_file_id)
        file.enable()
        return redirect(request.path)


@method_decorator(login_required, name='dispatch')
class ReportFileUploadView(View):

    def get(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        context = {
            'user': request.user,
            'profile': get_object_or_404(Profile, user=request.user),
            'report': report
        }

        return render(request, 'reports/modify_upload.html', context)

    def post(self, request, report_id):
        report = get_object_or_404(Report, user=request.user, report_id=report_id)
        form = ReportFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            name = 'file.pdf'
            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
                break

            uploaded_file = ReportFile.objects.create(
                user=request.user,
                report=report,
                file=form.cleaned_data.get('file'),
                commit_message=form.cleaned_data.get('commit_message'),
                filename=name
            )
            uploaded_file.save()

            if ReportFile.objects.filter(report=report).count() == 1:
                uploaded_file.enable()

        else:
            print(form.errors)
            return HttpResponse(status=400)

        return redirect(request.POST['next'])


@method_decorator(login_required, name='dispatch')
class ReportCreateView(View):
    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        report = Report.objects.create(
            user=request.user,
            authors=profile.name_kor,
            title='New Report ' + time.strftime("%Y.%m.%d %H.%M.%S"),
        )
        report.save()

        return redirect('reports_modify_info', report_id=report.report_id)

    def post(self, request):
        raise Http404


class DownloadView(View):
    def get(self, request, report_id):
        report = get_object_or_404(Report, report_id=report_id)
        file = get_object_or_404(ReportFile, report_id=report_id, enabled=True)
        is_permissioned_user = (request.user == report.user or request.user.is_superuser or request.user.is_staff)
        is_accessible_state = report.is_accessible or report.is_public

        if is_accessible_state or is_permissioned_user:
            file_path = os.path.join(settings.MEDIA_ROOT, file.file.path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/pdf")
                    response['Content-Disposition'] = 'attachment; filename=' + file.file.name
                    return response
            raise Http404
        else:
            raise Http404

    def post(self, request):
        raise Http404
