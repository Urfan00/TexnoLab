from django.urls import path
from .views import AboutView, contact, course_detail, course_list, error, index



urlpatterns = [
    path('error/', error),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', contact),
    path('course_list/', course_list),
    path('course_detail/', course_detail),
    path('', index, name='index'),
]
