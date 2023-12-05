from django.urls import path
from .views import TIMView


urlpatterns = [
    path('tim/', TIMView.as_view(), name='tim'),
]

