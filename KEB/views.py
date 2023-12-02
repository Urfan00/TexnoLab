from django.shortcuts import render
from django.views.generic import ListView
from Account.models import Account


class KEBView(ListView):
    model = Account
    template_name = 'keb-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keb"] = Account.objects.filter(is_graduate=True, is_keb=True, is_delete=False, is_superuser=False).all()
        return context
    

