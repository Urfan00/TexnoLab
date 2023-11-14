from Course.models import RequestUs
from Core.models import ContactUs

def base_data(request):
    data = {}

    data["is_view_false_count_request_us"] = RequestUs.objects.filter(is_view=False, is_delete=False).count()
    data["is_view_false_count_contact_us"] = ContactUs.objects.filter(is_view=False, is_delete=False).count()

    return data