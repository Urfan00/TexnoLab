from django.urls import path
from .views import (AdminBlogAddView,
                    AdminBlogEditView,
                    AdminBlogListView,
                    AdminCourseAddView,
                    AdminCourseEditView,
                    AdminCourseListView,
                    DashboardView)


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('course_dashboard/', AdminCourseListView.as_view(), name='course_dashboard'),
    path('course_edit/<slug:slug>', AdminCourseEditView.as_view(), name='course_edit'),
    path('course_add/', AdminCourseAddView.as_view(), name='course_add'),

    path('blog_dashboard/', AdminBlogListView.as_view(), name='blog_dashboard'),
    path('blog_edit/<slug:slug>', AdminBlogEditView.as_view(), name='blog_edit'),
    path('blog_add/', AdminBlogAddView.as_view(), name='blog_add'),


]

