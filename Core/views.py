from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from Account.models import Account
# from Account.views import FirstTimeLoginMixin
from Course.forms import RequestUsForm
from Course.models import Course, CourseStatistic
from Service.models import ServiceHome
from .forms import ContactFormModel, SubscribeForm
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
        context["partners"] = Partner.objects.filter(is_delete=False).all()
        context['blogs'] = Blog.objects.filter(is_delete=False).order_by('-date').all()[:4]
        context['courses'] = Course.objects.filter(is_delete=False).order_by('-start_date').all()[:8]
        context['main_menus'] = NavMenu.objects.filter(sub_menu__isnull=True).all()
        context['testimonials'] = Account.objects.filter(is_delete=False, feedback__isnull=False).order_by('?').all()[:5]
        context['sercice_home'] = ServiceHome.objects.order_by('-created_at')[:10]
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
            messages.success(request, 'Müraciətiniz uğurla göndərildi.')
            return redirect('index')  # Update with the appropriate view name
        return render(request, self.template_name, {'form': form, **self.get_context_data()})


class AboutView(ListView):
    model = AboutUs
    template_name = 'about-2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = AboutUs.objects.first()
        context['testimonials'] = Account.objects.filter(is_delete=False, feedback__isnull=False).order_by('?').all()[:5]
        return context


class ContactUsView(CreateView):
    template_name = 'contact-1.html'
    form_class = ContactFormModel
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["info"] = ContactInfo.objects.first()
        context['faqs'] = FAQ.objects.filter(is_delete=False).all()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Müraciətiniz uğurla göndərildi.')
        return super().form_valid(form)


def subscribe_view(request):
    current_path = request.META.get('HTTP_REFERER', '/')
    print( '===>>',current_path)

    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a success message or redirect the user to a thank you page
            return redirect(current_path)
    else:
        form = SubscribeForm()

    context = {'subscribe_form': form}
    return render(request, 'base.html', context)