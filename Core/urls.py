from django.urls import path
from .views import AboutView, ContactUsView, index



urlpatterns = [

    path('contact/', ContactUsView.as_view(), name='contact'),

    path('about/', AboutView.as_view(), name='about'),
    path('', index, name='index'),
]

handler404 = "Core.views.handler_not_found"
