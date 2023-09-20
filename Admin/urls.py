from django.urls import path
from .views import DashboardView, page2, page3


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('page2/', page2),
    path('page3/', page3),
]

