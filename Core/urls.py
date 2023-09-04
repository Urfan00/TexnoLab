from django.urls import path
from .views import about, blog, blog_detail, contact, course_detail, course_list, error, index



urlpatterns = [
    path('error/', error),
    path('about/', about),
    path('blog/', blog),
    path('blog_detail/', blog_detail),
    path('contact/', contact),
    path('course_list/', course_list),
    path('course_detail/', course_detail),
    path('index/', index),
]
