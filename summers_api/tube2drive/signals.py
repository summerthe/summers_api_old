import multiprocessing
import random
import traceback

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from summers_api.tube2drive.models import UploadRequest
from summers_api.tube2drive.utils import check_task_to_find_playlist_and_upload


@receiver(post_save, sender=UploadRequest)
def slugify_upload_request(sender, instance, *args, **kwargs):
    if kwargs["created"]:
        instance.slug = slugify(instance.playlist_id + str(random.randint(0, 9999)))
        instance.save()
        try:
            main_proces = multiprocessing.Process(
                target=check_task_to_find_playlist_and_upload,
                args=(
                    instance.playlist_id,
                    instance.folder_id,
                    instance.pk,
                ),
            )
            main_proces.start()
        except Exception:
            traceback.print_exc()
