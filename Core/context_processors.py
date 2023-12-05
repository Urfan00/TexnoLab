from Core.forms import SubscribeForm
from Service.models import Service
from .models import ContactInfo, NavMenu

def base_data(request):
    data = {}

    data['main_menus'] = NavMenu.objects.filter(sub_menu__isnull=True).all()
    data['services'] = Service.objects.filter(status=True, is_delete=False).all()
    data['contact'] = ContactInfo.objects.first()
    data['subscribe_form'] = SubscribeForm()
    return data
