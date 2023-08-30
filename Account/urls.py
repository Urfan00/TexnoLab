from django.urls import path
from .views import ChangePasswordView, LogInView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login/', LogInView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('change_password/', ChangePasswordView.as_view(), name = 'change_password'),
    # path('reset_password/', ResetPasswordView.as_view(), name = 'reset_password'),

]
