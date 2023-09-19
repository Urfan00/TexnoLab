from django.urls import path
from .views import page1, page2, page3


urlpatterns = [
    path('page1/', page1),
    path('page2/', page2),
    path('page3/', page3),
]

