from django.shortcuts import render
from django.views.generic import ListView
from .models import TIM, TIMImage, TIMVideo



class TIMView(ListView):
    model = TIM
    template_name = 'tim-list-1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tim'] = TIM.objects.filter(status=True, is_delete=False).first()
        context['tim_images'] = TIMImage.objects.filter(tim=context['tim']).all()
        context['tim_videos'] = TIMVideo.objects.filter(tim=context['tim']).all()

        return context
