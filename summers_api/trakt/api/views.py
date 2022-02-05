from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from base.apis import viewsets
from summers_api.trakt.models import Show, UsersShow

from .serializers import (
    MarkEpisodeSerializer,
    ShowCreateSerializer,
    ShowDetailSerializer,
    ShowUpdateSeasonSerializer,
)

User = get_user_model()


class ShowModelViewSet(viewsets.BaseModelViewSet):
    """
    Following Endpoints are created by this modelviewset.

    Create: POST `/`
    List: GET `/`
    Retrieve: GET `/<pk>/`
    Destroy: DELETE `/<pk>/`
    my: GET `/my/`
    wishlist: POST `/<pk>/wishlist/`
    season: PUT `/<pk>/season/`
    Mark episode: PUT `/<pk>/mark-episode/`
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [AllowAny]
    serializer_class = ShowDetailSerializer
    queryset = Show.objects.all()
    models = Show

    def get_serializer_class(self):
        if self.action == "create":
            return ShowCreateSerializer
        elif self.action == "mark_episode":
            return MarkEpisodeSerializer
        elif self.action == "season":
            return ShowUpdateSeasonSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        show = serializer.save()
        data = ShowDetailSerializer(instance=show, context={"request": request}).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # if current user is authenticated remove already added show and return
            usersshows = request.user.usersshow.all()
            queryset = Show.objects.exclude(usersshow__in=usersshows)
        else:
            # if current user is not authenticated return all
            queryset = super().get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def my(self, request, *args, **kwargs):
        # return all show of current user
        usersshows = request.user.usersshow.all()
        queryset = Show.objects.filter(usersshow__in=usersshows).order_by(
            "usersshow",
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def wishlist(self, request, *args, **kwargs):
        """Add show into wishlist"""
        user = self.request.user
        show = self.get_object()

        if not user.usersshow.filter(show=show).exists():
            UsersShow.objects.create(user=user, show=show)
            serializer = self.get_serializer(show, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            data = {"message": "Show is already added into wishlist"}
            return Response(data=data, status=status.HTTP_304_NOT_MODIFIED)

    @action(
        methods=["PUT"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="season",
    )
    def season(self, request, *args, **kwargs):
        """Add new season in show."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        show = self.get_object()
        show = serializer.save(show=show)
        data = ShowDetailSerializer(instance=show, context={"request": request}).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        methods=["PUT"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="mark-episode",
    )
    def mark_episode(self, request, *args, **kwargs):
        """Mark episode of show"""
        show = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={"request": request, "show": show},
        )
        serializer.is_valid(raise_exception=True)
        usersshow = serializer.save()
        return Response(
            data=ShowDetailSerializer(
                instance=usersshow.show,
                context={"request": request},
            ).data,
            status=status.HTTP_200_OK,
        )
