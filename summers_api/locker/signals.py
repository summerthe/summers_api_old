import random

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from summers_api.locker.models import Category, Folder, Note, Vault


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
