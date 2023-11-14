from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from Service.models import AllGalery, ServiceHome



@receiver(pre_delete, sender=AllGalery)
def delete_img_file(sender, instance, **kwargs):
    # Delete the img file when an instance is deleted
    instance.img.delete(False)
