import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from base.models import BaseModel

User = get_user_model()


# Create your models here.
class Category(BaseModel):

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["title"]


class Vault(BaseModel):
    """Workspace like model for one user that contains all folders and notes."""

    title = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="note/vault-icons/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name = _("Vault")
        verbose_name_plural = _("Vaults")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Folder(BaseModel):
    """Folder to hold notes within them."""

    title = models.CharField(max_length=255)
    is_pinned = models.BooleanField(default=False, blank=True)
    vault = models.ForeignKey(Vault, on_delete=models.CASCADE)
    icon = models.ImageField(upload_to="note/folder-icons/", null=True, blank=True)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title


class Note(BaseModel):
    """Single note instance"""

    SCRATCHPAD_NOTE_CHOICE = "SCRATCHPAD"
    DEFAULT_NOTE_CHOICE = "DEFAULT"
    FAVOURITE_NOTE_CHOICE = "FAVOURITE"
    TRASH_NOTE_CHOICE = "TRASH"

    NOTE_TYPE_CHOICES = (
        (SCRATCHPAD_NOTE_CHOICE, SCRATCHPAD_NOTE_CHOICE),
        (DEFAULT_NOTE_CHOICE, DEFAULT_NOTE_CHOICE),
        (FAVOURITE_NOTE_CHOICE, FAVOURITE_NOTE_CHOICE),
        (TRASH_NOTE_CHOICE, TRASH_NOTE_CHOICE),
    )

    title = models.CharField(
        max_length=255,
    )
    description = models.TextField()
    type = models.CharField(
        max_length=10,
        choices=NOTE_TYPE_CHOICES,
        default=DEFAULT_NOTE_CHOICE,
        blank=True,
    )
    is_pinned = models.BooleanField(default=False, blank=True)

    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True)

    bg_image = models.ImageField(upload_to="note/bg-images/", null=True, blank=True)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ["-is_pinned", "-created_at"]

    def __str__(self):
        return self.title
