import random

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from summers_api.locker.models import Category, Folder, Note, Vault

User = get_user_model()


@receiver(post_save, sender=User)
def setup_locker_instances(sender, instance, *args, **kwargs):
    """Create vault,folder and scrappad for new user."""
    if kwargs["created"]:
        vault = Vault.objects.create(title="New Vault", user=instance)
        folder = Folder.objects.create(title=Note.DEFAULT_NOTE_CHOICE, vault=vault)
        Note.objects.create(
            title="# Your quick note.",
            description="",
            folder=folder,
            type=Note.SCRATCHPAD_NOTE_CHOICE,
        )


@receiver(pre_save, sender=Category)
def slugify_category(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.title + str(random.randint(0, 9999)))


@receiver(pre_save, sender=Vault)
def slugify_vault(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.title + str(random.randint(0, 9999)))


@receiver(pre_save, sender=Folder)
def slugify_folder(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.title + str(random.randint(0, 9999)))


@receiver(pre_save, sender=Note)
def slugify_note(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.title + str(random.randint(0, 9999)))
