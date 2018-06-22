from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.views.generic import RedirectView
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from reports.models import Report
from community.models import NoticePostModel, CommunityPostModel

# Create your views here.

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



from webserver.models import ImageResourceModel, FileResourceModel
from webserver.forms import ImageUploadForm
from django.core.exceptions import ValidationError

class IndexView(View):
    def get(self, request):
        new_reports = Report.objects.filter(is_public=True).order_by('-created_date')[:19]
        new_notices = NoticePostModel.objects.filter(is_visible=True).order_by('-post_id')[:5]
        new_posts   = CommunityPostModel.objects.filter(is_visible=True).order_by('-post_id')[:5]
        return render(request, 'index.html', {
            'report_list' : new_reports,
            'notice_list' : new_notices,
            'post_list' : new_posts
        })

    def post(self, request):
        return HttpResponseNotFound


class ShortReportUrlView(RedirectView):
    def get_redirect_url(self, report_id):
        return reverse('reports_view', args=report_id)


def fail(request):
    return render(request, 'fail.html')


def handler404(request):
    return render(request, '404.html', status=404)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff or user.is_superuser), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CKEditorImageUploadApiView(View):
    def get(self, request):
        raise HttpResponseNotFound

    def post(self, request):
        try:
            file = request.FILES['upload']
            name = file.name
            image = ImageResourceModel.objects.create(user = request.user, image = file)
            response = {
                "uploaded" : 1,
                "fileName" : name,
                "url": image.image.url
            }
            return JsonResponse(response, status=200)
        except ValidationError as e:
            response = {
                "uploaded": 0,
                "error" :{
                    "message" : e.message
                }
            }
            return JsonResponse(response, status=400)



@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff or user.is_superuser), name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class CKEditorFileUploadApiView(View):
    def get(self, request):
        raise HttpResponseNotFound

    def post(self, request):
        try:
            file = request.FILES['upload']
            name = file.name
            file = FileResourceModel.objects.create(user = request.user, file = file)
            response = {
                "uploaded" : 1,
                "fileName" : name,
                "url": file.file.url
            }
            return JsonResponse(response, status=200)
        except ValidationError as e:
            response = {
                "uploaded": 0,
                "error" :{
                    "message" : e.message
                }
            }
            return JsonResponse(response, status=400)




