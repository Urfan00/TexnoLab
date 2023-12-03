from django.urls import path
from .views import ServiceGalery, ServiceView

urlpatterns = [
    path('service/<slug:slug>', ServiceView.as_view(), name='service'),
    path('service_galery/', ServiceGalery.as_view(), name='service_galery')
]
