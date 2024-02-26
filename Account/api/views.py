# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from ExamResult.models import Group, StudentResult
from .serializers import StudentSingleTopicResultSerializer
from django.db.models import Sum
from rest_framework import status




class ResultAPIView(APIView):
    def get(self, request):
        g_query = self.request.GET.get('state', '')
        if g_query:
            group_topics = Group.objects.filter(id=g_query, is_active=True).first()
            all_topics = group_topics.all_course_topics.all()

            # Retrieve student results for the given group
            students_all_results = StudentResult.objects.filter(s_r_group=g_query).values(
                'student__id', 'student__first_name', 'student__last_name').annotate(
                avg_total_point=Sum('total_point')).order_by('-avg_total_point')

            serialized_results = []
            for student_result in students_all_results:
                student_id = student_result['student__id']
                other_topics_total_points = []
                for topic in all_topics:
                    topic_result = StudentResult.objects.filter(student_id=student_id, exam_topics=topic).first()
                    if topic_result:
                        other_topics_total_points.append(topic_result.total_point)
                    else:
                        other_topics_total_points.append('-------')

                serialized_student_result = {
                    'student__id': student_id,
                    'student__first_name': student_result['student__first_name'],
                    'student__last_name': student_result['student__last_name'],
                    'avg_total_point': student_result['avg_total_point'],
                    'other_topics_total_points': other_topics_total_points
                }
                serialized_results.append(serialized_student_result)

            return Response({'all_results': serialized_results})
        else:
            return Response()



class StudentResultList(APIView):
    def get(self, request, format=None):
        g_query = request.GET.get('state')
        t_query = request.GET.get('t')

        if g_query and t_query:
            queryset = StudentResult.objects.filter(s_r_group=g_query, exam_topics=t_query).order_by('-total_point')
            serializer = StudentSingleTopicResultSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("Please provide both 'state' and 't' parameters.", status=status.HTTP_400_BAD_REQUEST)

