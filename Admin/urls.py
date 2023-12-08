from django.urls import path
from .views import (AdminAboutContactInfoListView,
                    AdminAboutUsEditView,
                    AdminAccountAddView,
                    AdminAccountDetailView,
                    AdminAccountEditView,
                    AdminAccountListView,
                    AdminAllCourseGalleryDeleteView,
                    AdminAllCourseGalleryListView,
                    AdminAllGalleryAddView,
                    AdminAllGalleryDeleteAllView,
                    AdminAllGalleryDeleteView,
                    AdminAllVideoGalleryAddView,
                    AdminAllVideoGalleryDeleteView,
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
                    AdminContactUSListView,
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
                    AdminCourseFeedbackListView,
                    AdminCourseGalleryAddView,
                    AdminCourseListView,
                    AdminCourseProgramAddView,
                    AdminCourseProgramDeleteView,
                    AdminCourseProgramEditView,
                    AdminCourseProgramUndeleteView,
                    AdminCourseFeedbackDetailView,
                    AdminCourseFeedbackDeleteView,
                    AdminCourseFeedbackUndeleteView,
                    AdminCourseStatisticListView,
                    AdminCourseVideoAddView,
                    AdminCourseVideoDeleteView,
                    AdminGroupAddView,
                    AdminGroupEditView,
                    AdminKEBDeleteView,
                    AdminKEBUndeleteView,
                    AdminRequestUsDeleteView,
                    AdminRequestUsDetailView,
                    AdminRequestUsUndeleteView,
                    AdminCourseUndeleteView,
                    AdminFAQAddView,
                    AdminFAQDeleteView,
                    AdminFAQEditView,
                    AdminFAQListView,
                    AdminFAQUndeleteView,
                    AdminPartnerAddView,
                    AdminPartnerDeleteView,
                    AdminPartnerEditView,
                    AdminPartnerListView,
                    AdminPartnerUndeleteView,
                    AdminServiceAddView,
                    AdminServiceDeleteView,
                    AdminServiceDetailView,
                    AdminServiceHomeAddView,
                    AdminServiceHomeDeleteView,
                    AdminServiceEditView,
                    AdminServiceHomeEditView,
                    AdminServiceImageAddView,
                    AdminServiceImageDeleteView,
                    AdminServiceListView,
                    AdminServiceHomeUndeleteView,
                    AdminAllGalleryListView,
                    AdminServiceUndeleteView,
                    AdminServiceVideoAddView,
                    AdminServiceVideoDeleteView,
                    AdminSubscriberDeleteView,
                    AdminSubscriberView,
                    AdminTIMImageAddView,
                    AdminTIMImageDeleteView,
                    AdminTIMListView,
                    AdminTIMMainEditView,
                    AdminTIMVideoAddView,
                    AdminTIMVideoDeleteView,
                    CourseStudentAddView,
                    CourseStudentDeleteView,
                    CourseStudentEditView,
                    DashboardView)


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Course & Course Category & Course Program
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

    # Course Program
    path('program_add/', AdminCourseProgramAddView.as_view(), name='program_add'),
    path('program_edit/<int:pk>', AdminCourseProgramEditView.as_view(), name='program_edit'),
    path('program/<int:pk>/delete/', AdminCourseProgramDeleteView.as_view(), name='program_delete'),
    path('program/<int:pk>/undelete/', AdminCourseProgramUndeleteView.as_view(), name='program_undelete'),

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

    # Service & Service Home
    path('service_dashboard/', AdminServiceListView.as_view(), name='service_dashboard'),

    # Service
    path('service_add/', AdminServiceAddView.as_view(), name='service_add'),
    path('service_edit/<int:pk>', AdminServiceEditView.as_view(), name='service_edit'),
    path('service/<int:pk>/delete/', AdminServiceDeleteView.as_view(), name='service_delete'),
    path('service/<int:pk>/undelete/', AdminServiceUndeleteView.as_view(), name='service_undelete'),
    path('service_look/<int:pk>', AdminServiceDetailView.as_view(), name='service_look'),

    # ************************************************************************************************************************
    # Service Home
    path('service_home_add/', AdminServiceHomeAddView.as_view(), name='service_home_add'),
    path('service_home_edit/<int:pk>', AdminServiceHomeEditView.as_view(), name='service_home_edit'),
    path('service_home/<int:pk>/delete/', AdminServiceHomeDeleteView.as_view(), name='service_home_delete'),
    path('service_home/<int:pk>/undelete/', AdminServiceHomeUndeleteView.as_view(), name='service_home_undelete'),


    # ************************************************************************************************************************
    # Service Image
    path('service_image_add/', AdminServiceImageAddView.as_view(), name='service_image_add'),
    path('delete_service_image/<int:image_id>/', AdminServiceImageDeleteView.as_view(), name='delete_service_image'),
    # ************************************************************************************************************************

    # ************************************************************************************************************************
    # Service Video
    path('service_video_add/', AdminServiceVideoAddView.as_view(), name='service_video_add'),
    path('delete_service_video/<int:image_id>/', AdminServiceVideoDeleteView.as_view(), name='delete_service_video'),
    # ************************************************************************************************************************

    # Course Statistic
    path('statistic_dashboard/', AdminCourseStatisticListView.as_view(), name='statistic_dashboard'),

    # ************************************************************************************************************************

    # Feedback
    path('feedback_dashboard/', AdminCourseFeedbackListView.as_view(), name='feedback_dashboard'),
    path('course_feedback_look/<int:pk>', AdminCourseFeedbackDetailView.as_view(), name='course_feedback_look'),
    path('feedback/<int:pk>/delete/', AdminCourseFeedbackDeleteView.as_view(), name='feedback_delete'),
    path('feedback/<int:pk>/undelete/', AdminCourseFeedbackUndeleteView.as_view(), name='feedback_undelete'),

    # ************************************************************************************************************************

    # Partner
    path('partner_dashboard/', AdminPartnerListView.as_view(), name='partner_dashboard'),
    path('partner_add/', AdminPartnerAddView.as_view(), name='partner_add'),
    path('partner_edit/<int:pk>', AdminPartnerEditView.as_view(), name='partner_edit'),
    path('partner/<int:pk>/delete/', AdminPartnerDeleteView.as_view(), name='partner_delete'),
    path('partner/<int:pk>/undelete/', AdminPartnerUndeleteView.as_view(), name='partner_undelete'),

    # ************************************************************************************************************************

    # FAQ
    path('faq_dashboard/', AdminFAQListView.as_view(), name='faq_dashboard'),
    path('faq_add/', AdminFAQAddView.as_view(), name='faq_add'),
    path('faq_edit/<int:pk>', AdminFAQEditView.as_view(), name='faq_edit'),
    path('faq/<int:pk>/delete/', AdminFAQDeleteView.as_view(), name='faq_delete'),
    path('faq/<int:pk>/undelete/', AdminFAQUndeleteView.as_view(), name='faq_undelete'),

    # ************************************************************************************************************************

    # Contact US
    path('apply_dashboard/', AdminContactUSListView.as_view(), name='apply_dashboard'),
    path('contact_us/<int:pk>/delete/', AdminContactUsDeleteView.as_view(), name='contact_us_delete'),
    path('contact_us/<int:pk>/undelete/', AdminContactUsUndeleteView.as_view(), name='contact_us_undelete'),
    path('contact_us/<int:pk>', AdminContactUsView.as_view(), name='contact_us_look'),

    # ************************************************************************************************************************

    # Request us
    path('request_us/<int:pk>/delete/', AdminRequestUsDeleteView.as_view(), name='request_us_delete'),
    path('request_us/<int:pk>/undelete/', AdminRequestUsUndeleteView.as_view(), name='request_us_undelete'),
    path('request_us/<int:pk>', AdminRequestUsDetailView.as_view(), name='request_us_look'),

    # ************************************************************************************************************************

    # About Us & Contact İnfo
    path('about_dashboard/', AdminAboutContactInfoListView.as_view(), name='about_dashboard'),

    path('about_us_edit', AdminAboutUsEditView.as_view(), name='about_us_edit'),
    path('contact_info_edit', AdminContactInfoEditView.as_view(), name='contact_info_edit'),

    # Account & Register & Group
    path('account_dashboard/', AdminAccountListView.as_view(), name='account_dashboard'),
    path('account_look/<int:pk>', AdminAccountDetailView.as_view(), name='account_look'),
    path('account_add/', AdminAccountAddView.as_view(), name='account_add'),
    path('account_edit/<int:pk>', AdminAccountEditView.as_view(), name='account_edit'),
    path('group_add/', AdminGroupAddView.as_view(), name='group_add'),
    path('group_edit/<int:pk>', AdminGroupEditView.as_view(), name='group_edit'),

    # Course Student
    path('course_student_add/', CourseStudentAddView.as_view(), name='course_student_add'),
    path('course_student_edit/<int:pk>', CourseStudentEditView.as_view(), name='course_student_edit'),
    path('course_student/<int:pk>/delete/', CourseStudentDeleteView.as_view(), name='course_student_delete'),

    # All Gallery
    path('gallery_dashboard/', AdminAllGalleryListView.as_view(), name='gallery_dashboard'),
    path('delete_image/<int:image_id>/', AdminAllGalleryDeleteView.as_view(), name='delete_image'),
    path('gallery_add/', AdminAllGalleryAddView.as_view(), name='gallery_add'),
    path('gallery_delete_all/', AdminAllGalleryDeleteAllView.as_view(), name='gallery_delete_all'),

 # ************************************************************************************************************************
    # Gallery Video
    path('gallery_video_add/', AdminAllVideoGalleryAddView.as_view(), name='gallery_video_add'),
    path('delete_video/<int:image_id>/', AdminAllVideoGalleryDeleteView.as_view(), name='delete_video'),
    # ************************************************************************************************************************

    # Subscriber
    path('subscribe_dashboard/', AdminSubscriberView.as_view(), name='subscribe_dashboard'),
    path('delete_email/<int:email_id>/', AdminSubscriberDeleteView.as_view(), name='delete_email'),

    # # KEB
    # path('keb_dashboard/', AdminKEBListView.as_view(), name='keb_dashboard'),
    path('keb/<int:pk>/delete/', AdminKEBDeleteView.as_view(), name='keb_delete'),
    path('keb/<int:pk>/undelete/', AdminKEBUndeleteView.as_view(), name='keb_undelete'),

    # Course Gallery
    path('course_gallery_dashboard/', AdminAllCourseGalleryListView.as_view(), name='course_gallery_dashboard'),
    path('delete_course_gallery_image/<int:image_id>/', AdminAllCourseGalleryDeleteView.as_view(), name='delete_course_gallery_image'),
    path('course_gallery_add/', AdminCourseGalleryAddView.as_view(), name='course_gallery_add'),

    # ************************************************************************************************************************
    # Course Image
    path('course_video_add/', AdminCourseVideoAddView.as_view(), name='course_video_add'),
    path('delete_course_video/<int:image_id>/', AdminCourseVideoDeleteView.as_view(), name='delete_course_video'),
    # ************************************************************************************************************************

    # TIM
    path('tim_dashboard/', AdminTIMListView.as_view(), name='tim_dashboard'),
    path('tim_main_edit/', AdminTIMMainEditView.as_view(), name='tim_main_edit'),

    path('tim_image_add/', AdminTIMImageAddView.as_view(), name='tim_image_add'),
    path('delete_tim_image/<int:image_id>/', AdminTIMImageDeleteView.as_view(), name='delete_tim_image'),

    path('tim_video_add/', AdminTIMVideoAddView.as_view(), name='tim_video_add'),
    path('delete_tim_video/<int:image_id>/', AdminTIMVideoDeleteView.as_view(), name='delete_tim_video'),


]
