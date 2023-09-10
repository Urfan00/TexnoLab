from django.urls import path
from .views import CourseDetailView, CourseListView


urlpatterns = [
    path('course/', CourseListView.as_view(), name='course'),
    path('course/<slug:slug>', CourseDetailView.as_view(), name='course')
]
