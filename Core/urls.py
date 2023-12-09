from django.urls import path
from .views import AboutView, CertificateView, ContactUsView, IndexView, subscribe_view



urlpatterns = [
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('', IndexView.as_view(), name='index'),
    path('certificate/', CertificateView.as_view(), name='certificate'),
    path('subscribe/', subscribe_view, name='subscribe'),

]


handler404 = "Core.views.handler_not_found"
