from Core.forms import SubscribeForm
from .models import NavMenu

def base_data(request):
    data = {}

    data['main_menus'] = NavMenu.objects.filter(sub_menu__isnull=True).all()

    data['subscribe_form'] = SubscribeForm()
    return data
