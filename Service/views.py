from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from Service.models import AllGalery, Service, ServiceImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



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
            context['service_images'] = ServiceImage.objects.filter(service=service, is_delete=False)
        else:
            # Handle the case where no matching service is found
            context['service'] = None
            context['service_images'] = None
        return context



class ServiceGalery(ListView):
    model = AllGalery
    template_name = 'gallery.html'
    context_object_name = 'galeries'
    paginate_by = 20

    def get_queryset(self):
        queryset = AllGalery.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        galeries = self.get_queryset()

        # Pagination
        page = self.request.GET.get('page')
        paginator = Paginator(galeries, self.paginate_by)

        try:
            galeries = paginator.page(page)
        except PageNotAnInteger:
            galeries = paginator.page(1)
        except EmptyPage:
            galeries = paginator.page(paginator.num_pages)

        context['galeries'] = galeries
        return context
