from Course.models import RequestUs
from Core.models import ContactUs

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
    return data