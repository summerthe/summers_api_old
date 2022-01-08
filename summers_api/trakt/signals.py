import random

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify

from .models import Show


@receiver(pre_save, sender=Show)
def slugify_show(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.slug = slugify(instance.title + str(random.randint(0, 9999)))
