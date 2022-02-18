from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Tube2DriveConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summers_api.tube2drive"
    verbose_name = _("Tube2Drive")
