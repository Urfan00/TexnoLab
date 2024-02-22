from Course.models import RequestUs
from Core.models import ContactUs
from ExamResult.models import CourseStudent
from Sxem.models import SxemStudent
from django.utils import timezone


def base_data(request):
    data = {}

    # Check if the user is authenticated, active, staff, and superuser
    if request.user.is_authenticated and request.user.is_active and request.user.is_staff and request.user.is_superuser:
        if request.user.image:
            data['superadmin_avatar'] = request.user.image.url
    else:
        data['superadmin_avatar'] = None

    data["is_view_false_count_request_us"] = RequestUs.objects.filter(is_view=False, is_delete=False).count()
    data["is_view_false_count_contact_us"] = ContactUs.objects.filter(is_view=False, is_delete=False).count()
    data['total_count'] = int(data["is_view_false_count_request_us"]) + int(data["is_view_false_count_contact_us"])

    if request.user.is_authenticated:
        if request.user.staff_status == 'Mentor' or request.user.staff_status == 'Müəllim':
            if request.user.staff_course.first():
                tm_course = request.user.staff_course.first().course
                if tm_course:
                    data['sxem_student_count'] = SxemStudent.objects.filter(sxem__course=tm_course, is_pass=False, is_student_answer=True).count()

    if request.user.is_authenticated:
        if request.user.staff_status == 'Tələbə':
            account_group = CourseStudent.objects.filter(
                student=request.user,
                group_student_is_active=True,
                is_keb = False,
                is_active = False,
                is_deleted = False,
                is_exam_group = True,
                group__is_active = True,
            ).first()
            if account_group:
                if request.user.exam_status:
                    current_time = timezone.now()
                    if account_group.group.exam_start_time < current_time and account_group.group.exam_end_time > current_time:
                        data['access_exam'] = True
                    else:
                        data['access_exam'] = False
                else:
                    data['access_exam'] = False
            else:
                data['access_exam'] = False

    return data
