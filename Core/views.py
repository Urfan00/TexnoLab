from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from Account.models import Account
from .models import AboutUs



def error(request):
    return render(request, '404.html')

def contact(request):
    return render(request, 'contact-1.html')

def course_list(request):
    return render(request, 'courses-list-5.html')

def course_detail(request):
    return render(request, 'courses-single-5.html')

def index(request):
    return render(request, 'home-3.html')


class AboutView(ListView):
    model = AboutUs
    template_name = 'about-2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutUs.objects.first()
        context['testimonials'] = Account.objects.order_by('?').all()[:5] # ad soyad testimonials bu 3 u ancaq !!!
        return context


