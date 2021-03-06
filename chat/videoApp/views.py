from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from .filters import *
from datetime import datetime
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from app.models import UserProfile
from .serializers import *
from .models import *


class VideoView(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class VideoCategoryView(viewsets.ModelViewSet):
    serializer_class = VideoCategorySerializer
    queryset = VideoCategory.objects.all()


def index(request):
    if request.method == "GET":
        return render(request, 'index.html')


class VideoList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'videos.html'

    def get(self, request):
        queryset = Video.objects.all()
        return Response({'videos': queryset})


class VideoDetail(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'video.html'

    def retrieve(self, request, pk, *args, **kwargs):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoSerializer(video)
        return Response({'serializer': serializer, 'video': video})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@csrf_exempt
def video_list(request, pk=None):

    if request.method == 'GET':
        if pk:
            videos = Video.objects.filter(id=pk)
        else:
            videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'categories.html'

    def get(self, request):
        queryset = Category.objects.all()
        return Response({'categories': queryset})


class CategoryDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category.html'

    def get(self, request, pk):
        videos = Video.objects.all()
        video_get = []
        category = Category.objects.get(pk=pk)
        for video in videos:
            if video == VideoCategory.objects.get(category=category).video:
                video_get.append(video)
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response({'serializer': serializer, 'category': category, 'videos': video_get})


class PostsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'video.add_video'
    template_name = 'video_create.html'
    form_class = PostsForm
    success_url = '/video/'


class SearchList(ListView):
    model = Video
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Video.objects.order_by('-create_date')
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = VideoFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        context['videos'] = list(Video.objects.filter(post__author__user=self.request.user))
        context['form'] = SearchForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


def author_view(request, pk):
    return render(request, 'page.html', {'id_user': pk,
                                         'receiver': User.objects.get(username=UserProfile.objects.get(id=pk).user.username),
                                         'userprofile': UserProfile.objects.get(id=pk),
                                         'avatar': UserProfile.objects.get(id=pk).avatar})


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category not in user.category_set.all():
        category.subscriber.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category in user.category_set.all():
        category.subscriber.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


