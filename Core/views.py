from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
from .forms import ContactFormModel
from .models import FAQ, AboutUs, ContactInfo
from django.contrib import messages



def error(request):
    return render(request, '404.html')

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


class ContactUsView(CreateView):
    template_name = 'contact-1.html'
    form_class = ContactFormModel
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info"] = ContactInfo.objects.first()
        context['faqs'] = FAQ.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been sent successfully!')
        return super().form_valid(form)