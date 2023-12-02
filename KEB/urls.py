from django.urls import path
from .views import KEBView



urlpatterns = [
    path('keb/', KEBView.as_view(), name='keb')
]
