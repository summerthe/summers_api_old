import random
import traceback

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from summers_api.tube2drive.models import UploadRequest
from summers_api.tube2drive.utils import find_playlist_and_upload


@receiver(pre_save, sender=UploadRequest)
def slugify_upload_request(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.playlist_id + str(random.randint(0, 9999)))
        try:
            find_playlist_and_upload(instance.playlist_id, instance.folder_id)
        except Exception:
            traceback.print_exc()
