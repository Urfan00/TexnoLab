from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
from Course.forms import RequestUsForm
from Course.models import Course, CourseStatistic
from .forms import ContactFormModel
from .models import FAQ, AboutUs, ContactInfo, NavMenu, Partner
from django.contrib import messages
from Blog.models import Blog



def handler_not_found(request, exception):
    return render(request, '404.html')

class IndexView(View):
    template_name = 'home-3.html'
    form_class = RequestUsForm

    def get_context_data(self):
        context = {}
        context["partners"] = Partner.objects.all()
        context['blogs'] = Blog.objects.order_by('-date').all()[:4]
        context['courses'] = Course.objects.order_by('-start_date').all()[:8]
        context['top_course'] = CourseStatistic.objects.order_by('-read_count').all()[:10]
        context['main_menus'] = NavMenu.objects.filter(sub_menu__isnull=True).all()
        context['testimonials'] = Account.objects.order_by('?').all()[:5] # ad soyad testimonials bu 3 u ancaq !!!
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, **self.get_context_data()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Optionally, you can add a success message or redirect to a different page
            messages.success(request, 'Form submission successful.')
            return redirect('index')  # Update with the appropriate view name
        return render(request, self.template_name, {'form': form, **self.get_context_data()})


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
