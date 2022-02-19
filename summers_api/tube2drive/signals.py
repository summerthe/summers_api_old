import random

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from summers_api.tube2drive.models import UploadRequest


@receiver(pre_save, sender=UploadRequest)
def slugify_upload_request(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.playlist_id + str(random.randint(0, 9999)))
