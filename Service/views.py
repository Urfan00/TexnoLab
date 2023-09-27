from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from Service.models import Service


# Create your views here.
class ServiceView(ListView):
    model = Service
    template_name = 'service-list-1.html'

    # def get_context_data(self, **kwargs):
        # context = super().get_context_data(**kwargs)
        # context['categories'] = BlogCategory.objects.filter(is_delete=False).all()
        # context['blogs'] = Blog.objects.filter(blog_category__is_delete=False, is_delete=False).all()
        # return context