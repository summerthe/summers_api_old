import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import gettext as _

from base.models import BaseModel

User = get_user_model()


class Show(BaseModel):

    title = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(upload_to="trakt/thumbnails/")
    categories = models.ManyToManyField("Category", blank=True)

    guid = models.UUIDField(_("guid"), default=uuid.uuid4, editable=False)
    slug = models.SlugField(unique=True, editable=False)

    @property
    def total_episodes(self):
        return (
            self.season_set.all()
            .aggregate(aggregrated_episodes=Sum("episode"))
            .get("aggregrated_episodes", 0)
        )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Show")
        verbose_name_plural = _("Shows")
        ordering = ["-updated_at"]


class Season(BaseModel):

    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    season = models.PositiveIntegerField(default=1)
    episode = models.PositiveIntegerField(default=8)

    def __str__(self):
        return self.show.title + "-" + str(self.season)

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        ordering = ["-show__updated_at", "season"]


class UsersShow(BaseModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usersshow")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="usersshow")
    watched_episode = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.user.username + "-" + self.show.title

    class Meta:
        verbose_name = _("User's show")
        verbose_name_plural = _("User's shows")
        ordering = ["-updated_at"]


class Category(BaseModel):

    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["title"]
