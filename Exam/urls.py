from django.urls import path
from .views import ExamResultView, QuizView, RuleView


urlpatterns = [
    path('quiz_rule/', RuleView.as_view(), name='quiz_rule'),
    path('quiz/', QuizView.as_view(), name='quiz'),
    path('exam_result/', ExamResultView.as_view(), name='exam_result'),
]
