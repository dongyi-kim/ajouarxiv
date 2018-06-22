from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.views import  View
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from django.http import HttpResponseNotFound, Http404, HttpResponseRedirect

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

from community.models import *
from accounts.models import Profile
from django.db.models import Q

import bleach
from urllib.parse import urlencode

from ajouarxiv import settings

class StudentCouncilListView(ListView):
    model = StudentCouncilModel
    template_name = 'community/council.html'
    paginate_by = 200
    ordering = ['-id']
    context_object_name = 'card_list'

class StudyClubListView(ListView):
    model = StudyClubModel
    template_name = 'community/club.html'
    paginate_by = 200
    ordering = ['-id']
    context_object_name = 'card_list'


class GalleryView(View):
    def get(self, request):
        return render(request, 'community/gallery.html', {})

    def post(self, request):
        return HttpResponseNotFound


class PostView(DetailView):
    model = CommunityPostModel
    template_name = 'community/post_view.html'
    context_object_name = 'post'

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model =  CommunityPostModel
    form_class = CommunityPostForm
    template_name = 'community/post_write.html'
    success_url = 'community_post_view'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(PostCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(viewname=self.success_url, kwargs={'pk':self.object.post_id})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = CommunityPostModel
    template_name = 'community/post_write.html'
    form_class = CommunityPostForm
    context_object_name = 'post'
    success_url = 'community_post_view'

    def get_object(self, queryset=None):
        # 자기 자신의 게시글만 접근 가능

        obj = super(PostUpdateView, self).get_object(queryset)

        if obj and (obj.user == self.request.user or self.request.user.is_superuser) :
            return obj

        raise HttpResponseNotFound

    def get_success_url(self):
        return reverse(viewname=self.success_url, kwargs={'pk':self.object.post_id})



class PostListView(ListView):
    model = CommunityPostModel
    template_name = 'community/post_list.html'
    paginate_by = 20
    context_object_name = 'post_list'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = urlencode(query_params)

        filter = {   }
        if self.request.GET.get('user'):
            filter['user'] = self.request.GET.get('user')

        if self.request.GET.get('post_title'):
            filter['title'] = self.request.GET.get('post_title')

        if self.request.GET.get('post_content'):
            filter['content'] = self.request.GET.get('post_content')

        context['filter'] = filter
        return context

    def get_queryset(self):
        queryset = self.model.objects
        if self.request.user.is_authenticated :
            if self.request.user.is_superuser or self.request.user.is_staff:
                queryset = queryset.all()
            if not self.request.user.is_staff and not self.request.user.is_superuser:
                queryset = queryset.filter(Q(is_visible=True) | Q(user=self.request.user))
        else:
            queryset = queryset.filter(is_visible=True)

        if self.request.GET.get('user'):
            pattern = self.request.GET.get('user').strip()
            users = User.objects.filter(username__contains=pattern)
            profiels = Profile.objects.filter(name_kor__contains=pattern).values_list('user', flat=True)

            queryset=queryset.filter(Q(user__in=users) | Q(user__in=set(profiels)))

        if self.request.GET.get('post_title'):
            pattern = self.request.GET.get('post_title')
            queryset=queryset.filter(post_title__contains=pattern)

        if self.request.GET.get('post_content'):
            pattern = self.request.GET.get('post_content')
            queryset=queryset.filter(post_content__contains=pattern)

        return queryset.order_by('-post_id')



class NoticeView(DetailView):
    model = NoticePostModel
    template_name = 'community/notice_view.html'
    context_object_name = 'post'


class NoticeListView(PostListView):
    model = NoticePostModel
    template_name = 'community/notice_list.html'
    paginate_by = 20
    context_object_name = 'notice_list'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff or user.is_superuser), name='dispatch')
class NoticeCreateView(PostCreateView):
    model =  NoticePostModel
    form_class = NoticePostForm
    template_name = 'community/notice_write.html'
    success_url = 'community_notice_view'


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_staff or user.is_superuser), name='dispatch')
class NoticeUpdateView(PostUpdateView):
    model = NoticePostModel
    template_name = 'community/notice_write.html'
    success_url = 'community_notice_view'
    form_class = NoticePostForm



