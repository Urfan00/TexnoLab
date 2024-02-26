from django.urls import path
from Account.api.views import ResultAPIView, StudentResultList
from .views import AccountInformationView, ChangePasswordView, LogInView, ResetPasswordConfirmView, ResetPasswordView, ResultView, logout_view
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', logout_view, name='logout'),


    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_confirm/<str:uidb64>/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),

    path('profile/', AccountInformationView.as_view(), name='profile'),
    path('result/', ResultView.as_view(), name='result'),

    path('api/results/', ResultAPIView.as_view(), name='api_results'),
    path('api/students_results/', StudentResultList.as_view(), name='student_results_api'),

]
