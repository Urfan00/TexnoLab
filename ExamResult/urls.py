from django.urls import path
from .views import ExamStart, GiveLabPointView, GivePointView, MentorLabEvaluationView, SaveExamView, TeacherEvaluationView



urlpatterns = [
    path('exam_start/', ExamStart.as_view(), name='exam_start'),
    path('save_exam/', SaveExamView.as_view(), name='save_exam'),

    path('evaluation/', TeacherEvaluationView.as_view(), name='evaluation'),
    path('give_point/<int:student_id>/<int:group_id>', GivePointView.as_view(), name='give_point'),

    path('lab_evaluation/', MentorLabEvaluationView.as_view(), name='lab_evaluation'),
    path('mentor_evaluation/', GiveLabPointView.as_view(), name='mentor_evaluation'),
]
