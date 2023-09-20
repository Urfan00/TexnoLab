from django.urls import path
from .views import AdminCourseAddView, AdminCourseEditView, AdminCourseListView, DashboardView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('course_dashboard/', AdminCourseListView.as_view(), name='course_dashboard'),
    path('course_edit/<slug:slug>', AdminCourseEditView.as_view(), name='course_edit'),
    path('course_add/', AdminCourseAddView.as_view(), name='course_add'),

]

