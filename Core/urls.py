from django.urls import path
from .views import AboutView, ContactUsView, course_detail, course_list, index



urlpatterns = [

    path('contact/', ContactUsView.as_view(), name='contact'),

    path('about/', AboutView.as_view(), name='about'),
    path('course_list/', course_list),
    path('course_detail/', course_detail),
    path('', index, name='index'),
]

handler404 = "Core.views.handler_not_found"
