from django.urls import path
from .views import ServiceGalery, ServiceListView, ServiceView, servicecoursetim

urlpatterns = [
    path('service', ServiceListView.as_view(), name='service'),
    path('service/<slug:slug>', ServiceView.as_view(), name='service'),
    path('service_galery/', ServiceGalery.as_view(), name='service_galery'),
    path('all_service/', servicecoursetim, name='all_service')
]
