import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from base.models import BaseModel

User = get_user_model()


# Create your models here.
class UploadRequest(BaseModel):
    START_CHOICE = "START"
    RUNNING_CHOICE = "RUNNING"
    COMPLETED_CHOICE = "COMPLETED"
    FAILED_CHOICE = "FAILED"
    NOT_FOUND_CHOICE = "NOT_FOUND"

    STATUS_CHOICES = (
        (START_CHOICE, START_CHOICE),
        (RUNNING_CHOICE, RUNNING_CHOICE),
        (COMPLETED_CHOICE, COMPLETED_CHOICE),
        (FAILED_CHOICE, FAILED_CHOICE),
        (NOT_FOUND_CHOICE, NOT_FOUND_CHOICE),
    )

    playlist_id = models.CharField(max_length=255)
    folder_id = models.CharField(max_length=255)
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=9,
        default=START_CHOICE,
        blank=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.playlist_id

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["-updated_at"]
