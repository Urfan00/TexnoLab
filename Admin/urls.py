from django.urls import path
from .views import (AdminBlogAddView,
                    AdminBlogCategoryAddView,
                    AdminBlogCategoryDeleteView,
                    AdminBlogCategoryEditView,
                    AdminBlogCategoryUndeleteView,
                    AdminBlogDeleteView,
                    AdminBlogEditView,
                    AdminBlogListView,
                    AdminBlogUndeleteView,
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

    path('blog_category_edit/<int:pk>', AdminBlogCategoryEditView.as_view(), name='blog_category_edit'),
    path('blog_category_add/', AdminBlogCategoryAddView.as_view(), name='blog_category_add'),

    path('blog/<slug:slug>/delete/', AdminBlogDeleteView.as_view(), name='blog_delete'),
    path('blog-category/<int:pk>/delete/', AdminBlogCategoryDeleteView.as_view(), name='blog_category_delete'),

    path('blog/<slug:slug>/undelete/', AdminBlogUndeleteView.as_view(), name='blog_undelete'),
    path('blog-category/<int:pk>/undelete/', AdminBlogCategoryUndeleteView.as_view(), name='blog_category_undelete'),  # Add undelete URL



]

