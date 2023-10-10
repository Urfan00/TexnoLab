from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from Service.models import Service, ServiceImage


# Create your views here.
class ServiceView(ListView):
    model = Service
    template_name = 'service-list-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service = Service.objects.filter(status=True, is_delete=False).first()
        print(service)

        # If a service is found, filter its associated ServiceImage objects
        if service:
            context['service'] = service
            context['service_images'] = ServiceImage.objects.filter(service=service)
        else:
            # Handle the case where no matching service is found
            context['service'] = None
            context['service_images'] = None
        return context
