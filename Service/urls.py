from django.urls import path
from .views import ServiceGalery, ServiceView

urlpatterns = [
    path('service/', ServiceView.as_view(), name='service'),
    path('service_galery/', ServiceGalery.as_view(), name='service_galery')
]
