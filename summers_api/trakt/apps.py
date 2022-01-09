from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _


class TraktConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "summers_api.trakt"
    verbose_name = _("Trakt")

    def ready(self) -> None:
        from summers_api.trakt.models import Show
        from summers_api.trakt.signals import slugify_show  # noqa E402

        pre_save.connect(slugify_show, sender=Show)
