from django.urls import path
from .views import BlogDetailView, BlogView


urlpatterns = [
    path('blog/', BlogView.as_view(), name='blog'),
    path('blog/<slug:slug>', BlogDetailView.as_view(), name='blog'),
]
