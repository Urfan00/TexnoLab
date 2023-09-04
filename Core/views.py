from django.shortcuts import render


def error(request):
    return render(request, '404.html')

def about(request):
    return render(request, 'about-2.html')

def blog(request):
    return render(request, 'blog-list-1.html')

def blog_detail(request):
    return render(request, 'blog-single.html')

def contact(request):
    return render(request, 'contact-1.html')

def course_list(request):
    return render(request, 'courses-list-6.html')

def course_detail(request):
    return render(request, 'courses-single-5.html')

def index(request):
    return render(request, 'home-3.html')
