from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


class Tube2DriveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summers_api.tube2drive"
    verbose_name = _("Tube2Drive")

    def ready(self) -> None:

        from summers_api.tube2drive.models import UploadRequest
        from summers_api.tube2drive.signals import slugify_upload_request

        post_save.connect(slugify_upload_request, sender=UploadRequest)
