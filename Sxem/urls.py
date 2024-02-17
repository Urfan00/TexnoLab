from django.urls import path
from .views import SxemDetailView, SxemListView, SxemTeacherMentorEvaluationView, SxemTeacherMentorListView


urlpatterns = [
    path("sxem_list/", SxemListView.as_view(), name="sxem_list"),
    path("sxem_detail/<int:pk>", SxemDetailView.as_view(), name="sxem_detail"),
    path('sxem_tm/', SxemTeacherMentorListView.as_view(), name='sxem_tm'),
    path("sxem_tm_detail/<int:pk>", SxemTeacherMentorEvaluationView.as_view(), name="sxem_tm_detail"),
]
