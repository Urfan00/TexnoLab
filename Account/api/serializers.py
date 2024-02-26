# serializers.py
from rest_framework import serializers
from ExamResult.models import StudentResult



class StudentResultSerializer(serializers.ModelSerializer):
    other_topics_total_points = serializers.SerializerMethodField()

    class Meta:
        model = StudentResult
        fields = ('student__id', 'student__first_name', 'student__last_name', 'avg_total_point', 'other_topics_total_points')

    def get_other_topics_total_points(self, obj):
        all_topics = obj.s_r_group.all_course_topics.all()
        student_id = obj.student_id
        other_topics_total_points = []
        for topic in all_topics:
            topic_result = StudentResult.objects.filter(student_id=student_id, exam_topics=topic).first()
            if topic_result:
                other_topics_total_points.append(topic_result.total_point)
            else:
                other_topics_total_points.append('-------')
        return other_topics_total_points



class StudentSingleTopicResultSerializer(serializers.ModelSerializer):
    student_full_name = serializers.SerializerMethodField()
    exam_topic_title = serializers.SerializerMethodField()
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = StudentResult
        fields = ('student', 'student_full_name', 'total_point', 'exam_topic_title', 's_r_group', 'created_at_formatted')

    def get_student_full_name(self, obj):
        return obj.student.get_full_name() if obj.student else None

    def get_exam_topic_title(self, obj):
        return obj.exam_topics.topic_title if obj.exam_topics else None

    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime('%d.%m.%Y') if obj.created_at else None
