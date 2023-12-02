from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Blog, BlogCategory



class BlogView(ListView):
    model = Blog
    template_name = 'blog-list-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_delete=False).all()
        context['blogs'] = Blog.objects.filter(status=True, blog_category__is_delete=False, is_delete=False).all()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog-single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.filter(is_delete=False).all()
        context['related_blogs'] = Blog.objects.filter(status=True, blog_category = self.object.blog_category, blog_category__is_delete=False, is_delete=False).exclude(slug=self.kwargs.get('slug'))[:4]
        return context

