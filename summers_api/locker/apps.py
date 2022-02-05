from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _


class LockerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summers_api.locker"
    verbose_name = _("Locker")

    def ready(self) -> None:
        from summers_api.locker.models import Category, Folder, Note, Vault
        from summers_api.locker.signals import (
            slugify_category,
            slugify_folder,
            slugify_note,
            slugify_vault,
        )

        pre_save.connect(slugify_category, sender=Category)
        pre_save.connect(slugify_vault, sender=Vault)
        pre_save.connect(slugify_folder, sender=Folder)
        pre_save.connect(slugify_note, sender=Note)
