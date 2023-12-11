from random import shuffle
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from Service.models import AllGalery, AllVideoGallery, Service, ServiceImage, ServiceVideo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.
class ServiceView(DetailView):
    model = Service
    template_name = 'service-list-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_images'] = ServiceImage.objects.filter(service=self.object).all()
        context['service_videos'] = ServiceVideo.objects.filter(service=self.object).all()

        return context


class ServiceGalery(ListView):
    model = AllGalery
    template_name = 'gallery.html'
    context_object_name = 'galeries'
    paginate_by = 30

    def get_queryset(self):
        queryset = AllGalery.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = AllVideoGallery.objects.all()
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


def servicecoursetim(request):
    return render(request, 'service-course-tim.html')


class ServiceListView(ListView):
    model = Service
    template_name = 'service-in.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.filter(status=True, is_delete=False).all()
        return context

