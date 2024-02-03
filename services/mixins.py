from django.db import models
from django.shortcuts import redirect, render


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# ***************************************************************
# USER - MIXINS

# ONLY SuperUser
class AuthSuperUserMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'SuperUser':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY Müəllim
class AuthTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'Müəllim':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY Mentor
class AuthMentorMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is mentor
            if request.user.staff_status == 'Mentor':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not mentor, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY Koordinator
class AuthCoordinatorMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is mentor
            if request.user.staff_status == 'Koordinator':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not mentor, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY Tələbə
class AuthStudentPageMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is mentor
            if request.user.staff_status == 'Tələbə':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not mentor, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY SuperUser & Müəllim
class AuthSuperUserTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'SuperUser' or request.user.staff_status == 'Müəllim':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY SuperUser & Koordinator
class AuthSuperUserCoordinatorMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'SuperUser' or request.user.staff_status == 'Koordinator':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')


# ONLY SuperUser & Koordinator & Müəllim
class AuthSuperUserCoordinatorTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user is teacher
            if request.user.staff_status == 'SuperUser' or request.user.staff_status == 'Koordinator' or request.user.staff_status == 'Müəllim':
                return super().dispatch(request, *args, **kwargs)
            else:
                # User is authenticated but not teacher, redirect to 404 page
                return render(request, '404.html')
        else:
            # User is not authenticated, redirect to login page
            return redirect('login')

