from django.urls import path
from .views import (AdminAboutContactInfoListView,
                    AdminAboutUsEditView,
                    AdminBlogAddView,
                    AdminBlogCategoryAddView,
                    AdminBlogCategoryDeleteView,
                    AdminBlogCategoryEditView,
                    AdminBlogCategoryUndeleteView,
                    AdminBlogDeleteView,
                    AdminBlogEditView,
                    AdminBlogListView,
                    AdminBlogUndeleteView,
                    AdminContactInfoEditView,
                    AdminContactUSFAQPartnersListView,
                    AdminContactUsDeleteView,
                    AdminContactUsUndeleteView,
                    AdminContactUsView,
                    AdminCourseAddView,
                    AdminCourseCategoryAddView,
                    AdminCourseCategoryDeleteView,
                    AdminCourseCategoryEditView,
                    AdminCourseCategoryUndeleteView,
                    AdminCourseDeleteView,
                    AdminCourseEditView,
                    AdminCourseListView,
                    AdminCourseProgramAddView,
                    AdminCourseProgramDeleteView,
                    AdminCourseProgramEditView,
                    AdminCourseProgramUndeleteView,
                    AdminCourseSRFPDetailView,
                    AdminCourseSRFPFeedbackDeleteView,
                    AdminCourseSRFPFeedbackUndeleteView,
                    AdminCourseSRFPListView,
                    AdminCourseSRFPRequestUsDeleteView,
                    AdminCourseSRFPRequestUsDetailView,
                    AdminCourseSRFPRequestUsUndeleteView,
                    AdminCourseUndeleteView,
                    AdminFAQAddView,
                    AdminFAQDeleteView,
                    AdminFAQEditView,
                    AdminFAQUndeleteView,
                    AdminPartnerAddView,
                    AdminPartnerDeleteView,
                    AdminPartnerEditView,
                    AdminPartnerUndeleteView,
                    AdminServiceAddView,
                    AdminServiceDeleteView,
                    AdminServiceEditView,
                    AdminServiceListView,
                    AdminServiceUndeleteView,
                    DashboardView)


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Course & Course Category
    path('course_dashboard/', AdminCourseListView.as_view(), name='course_dashboard'),

    # Course
    path('course_edit/<slug:slug>', AdminCourseEditView.as_view(), name='course_edit'),
    path('course_add/', AdminCourseAddView.as_view(), name='course_add'),
    path('course/<int:pk>/delete/', AdminCourseDeleteView.as_view(), name='course_delete'),
    path('course/<int:pk>/undelete/', AdminCourseUndeleteView.as_view(), name='course_undelete'),

    # ************************************************************************************************************************

    # Course Category
    path('course_category_edit/<int:pk>', AdminCourseCategoryEditView.as_view(), name='course_category_edit'),
    path('course_category_add/', AdminCourseCategoryAddView.as_view(), name='course_category_add'),
    path('course_category/<int:pk>/delete/', AdminCourseCategoryDeleteView.as_view(), name='course_category_delete'),
    path('course_category/<int:pk>/undelete/', AdminCourseCategoryUndeleteView.as_view(), name='course_category_undelete'),

    # ************************************************************************************************************************

    # Blog & Category
    path('blog_dashboard/', AdminBlogListView.as_view(), name='blog_dashboard'),

    # Blog
    path('blog_edit/<slug:slug>', AdminBlogEditView.as_view(), name='blog_edit'),
    path('blog_add/', AdminBlogAddView.as_view(), name='blog_add'),
    path('blog/<int:pk>/delete/', AdminBlogDeleteView.as_view(), name='blog_delete'),
    path('blog/<int:pk>/undelete/', AdminBlogUndeleteView.as_view(), name='blog_undelete'),

    # ************************************************************************************************************************

    # Blog Category
    path('blog_category_edit/<int:pk>', AdminBlogCategoryEditView.as_view(), name='blog_category_edit'),
    path('blog_category_add/', AdminBlogCategoryAddView.as_view(), name='blog_category_add'),
    path('blog-category/<int:pk>/delete/', AdminBlogCategoryDeleteView.as_view(), name='blog_category_delete'),
    path('blog-category/<int:pk>/undelete/', AdminBlogCategoryUndeleteView.as_view(), name='blog_category_undelete'),

    # ************************************************************************************************************************

    # Service
    path('service_dashboard/', AdminServiceListView.as_view(), name='service_dashboard'),
    path('service_add/', AdminServiceAddView.as_view(), name='service_add'),
    path('service_edit/<slug:slug>', AdminServiceEditView.as_view(), name='service_edit'),
    path('service/<int:pk>/delete/', AdminServiceDeleteView.as_view(), name='service_delete'),
    path('service/<int:pk>/undelete/', AdminServiceUndeleteView.as_view(), name='service_undelete'),

    # ************************************************************************************************************************

    # Course Statistic & Feedback & & Request us & Program
    path('course_srfp/', AdminCourseSRFPListView.as_view(), name='course_srfp'),

    # Feedback
    path('course_srfp_look/<int:pk>', AdminCourseSRFPDetailView.as_view(), name='course_srfp_look'),
    path('feedback/<int:pk>/delete/', AdminCourseSRFPFeedbackDeleteView.as_view(), name='feedback_delete'),
    path('feedback/<int:pk>/undelete/', AdminCourseSRFPFeedbackUndeleteView.as_view(), name='feedback_undelete'),

    # Request us
    path('request_us/<int:pk>/delete/', AdminCourseSRFPRequestUsDeleteView.as_view(), name='request_us_delete'),
    path('request_us/<int:pk>/undelete/', AdminCourseSRFPRequestUsUndeleteView.as_view(), name='request_us_undelete'),
    path('request_us/<int:pk>', AdminCourseSRFPRequestUsDetailView.as_view(), name='request_us_look'),

    # Course Program
    path('program_add/', AdminCourseProgramAddView.as_view(), name='program_add'),
    path('program_edit/<int:pk>', AdminCourseProgramEditView.as_view(), name='program_edit'),
    path('program/<int:pk>/delete/', AdminCourseProgramDeleteView.as_view(), name='program_delete'),
    path('program/<int:pk>/undelete/', AdminCourseProgramUndeleteView.as_view(), name='program_undelete'),

    # Partner & Contact US & FAQ
    path('core_dashboard/', AdminContactUSFAQPartnersListView.as_view(), name='core_dashboard'),

    # Partner
    path('partner_add/', AdminPartnerAddView.as_view(), name='partner_add'),
    path('partner_edit/<int:pk>', AdminPartnerEditView.as_view(), name='partner_edit'),
    path('partner/<int:pk>/delete/', AdminPartnerDeleteView.as_view(), name='partner_delete'),
    path('partner/<int:pk>/undelete/', AdminPartnerUndeleteView.as_view(), name='partner_undelete'),

    # FAQ
    path('faq_add/', AdminFAQAddView.as_view(), name='faq_add'),
    path('faq_edit/<int:pk>', AdminFAQEditView.as_view(), name='faq_edit'),
    path('faq/<int:pk>/delete/', AdminFAQDeleteView.as_view(), name='faq_delete'),
    path('faq/<int:pk>/undelete/', AdminFAQUndeleteView.as_view(), name='faq_undelete'),

    # Contact us
    path('contact_us/<int:pk>/delete/', AdminContactUsDeleteView.as_view(), name='contact_us_delete'),
    path('contact_us/<int:pk>/undelete/', AdminContactUsUndeleteView.as_view(), name='contact_us_undelete'),
    path('contact_us/<int:pk>', AdminContactUsView.as_view(), name='contact_us_look'),


    # About Us & Contact İnfo
    path('about_dashboard/', AdminAboutContactInfoListView.as_view(), name='about_dashboard'),

    path('about_us_edit', AdminAboutUsEditView.as_view(), name='about_us_edit'),
    path('contact_info_edit', AdminContactInfoEditView.as_view(), name='contact_info_edit'),

]

