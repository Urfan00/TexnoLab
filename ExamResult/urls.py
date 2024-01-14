from django.urls import path
from .views import ExamStart, SaveExamView



urlpatterns = [
    path('exam_start/', ExamStart.as_view(), name='exam_start'),
    path('save_exam/', SaveExamView.as_view(), name='save_exam'),

]
