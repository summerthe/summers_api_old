from django.contrib.auth import get_user_model
from django.db.models.aggregates import Max
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from summers_api.trakt.models import Category, Season, Show, UsersShow

User = get_user_model()


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title"]


class SeasonSerializer(ModelSerializer):
    class Meta:
        model = Season
        fields = ["season", "episode"]


class ShowCreateSerializer(ModelSerializer):
    categories = CategorySerializer(many=True, required=False)

    class Meta:
        model = Show
        fields = [
            "title",
            "thumbnail",
            "categories",
        ]

    def save(self):
        data_title = self._validated_data["title"]
        data_thumbnail = self._validated_data["thumbnail"]
        data_categories = self._validated_data.get("categories", None)

        if data_categories:
            categories = [
                Category.objects.get_or_create(data_category.get("title"))
                for data_category in data_categories
            ]
        else:
            categories = None

        show = Show.objects.create(title=data_title, thumbnail=data_thumbnail)
        if categories:
            show.categories.set(categories)
        return show


class ShowDetailSerializer(ModelSerializer):
    wishlisted = SerializerMethodField()
    seasons = SerializerMethodField()
    watched_episode = SerializerMethodField()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Show
        fields = [
            "id",
            "guid",
            "title",
            "thumbnail",
            "slug",
            "wishlisted",
            "watched_episode",
            "categories",
            "seasons",
            "created_at",
            "updated_at",
        ]

    def get_wishlisted(self, obj):
        user = self.context["request"].user
        if isinstance(user, User):
            return obj.usersshow.filter(user=user).exists()
        return False

    def get_watched_episode(self, obj):
        user = self.context["request"].user
        if isinstance(user, User):
            try:
                return obj.usersshow.get(user=user).watched_episode
            except UsersShow.DoesNotExist:
                pass
        return 0

    def get_seasons(self, obj):
        return (
            obj.season_set.all()
            .values("season")
            .annotate(total_episodes=Max("episode"))
        )


class ShowUpdateSeasonSerializer(ModelSerializer):
    seasons = SeasonSerializer(many=True)

    class Meta:
        model = Show
        fields = [
            "seasons",
        ]

    def save(self, show):
        data_seasons = self._validated_data["seasons"]
        Season.objects.bulk_create(
            [
                Season(
                    show=show,
                    season=season.get("season"),
                    episode=season.get("episode"),
                )
                for season in data_seasons
            ],
        )
        return show


class MarkEpisodeSerializer(serializers.Serializer):
    episode = serializers.IntegerField(min_value=1)

    def save(self, **kwargs):
        request = self.context.get("request")
        show = self.context.get("show")

        # if user has added current show then update total_episode
        if show and request.user.usersshow.filter(show=show).exists():
            usersshow = request.user.usersshow.get(show=show)
            episode = self.validated_data["episode"]
            total_episodes = show.total_episodes
            usersshow.watched_episode = (
                total_episodes if episode > total_episodes else episode
            )
            usersshow.save()
            return usersshow
        else:
            raise NotFound({"show": "User hasn't added show in wishlist"})
