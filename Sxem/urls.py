from django.urls import path
from .views import SxemDetailView, SxemListView


urlpatterns = [
    path("sxem_list/", SxemListView.as_view(), name="sxem_list"),
    path("sxem_detail/<int:pk>", SxemDetailView.as_view(), name="sxem_detail")
]
