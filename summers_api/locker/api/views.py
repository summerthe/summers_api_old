from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.settings import api_settings as drf_settings

from base.apis import viewsets
from summers_api.locker.api.permissions import (
    VaultAndFolderOwnPermission,
    VaultOwnPermission,
)
from summers_api.locker.api.serializers import (
    CategorySerializer,
    FolderSerializer,
    NoteSerializer,
    NoteUpdateSerializer,
    VaultSerializer,
)
from summers_api.locker.models import Category, Folder, Note, Vault


class CategoryViewSet(viewsets.BaseCreateListRetrieveModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    @action(
        detail=True,
        methods=["get"],
        url_path="notes",
        permission_classes=[VaultOwnPermission],
    )
    def note(self, request, *args, **kwargs):
        vault_id = request.GET.get("vault_id")
        qs = Note.objects.filter(folder__vault_id=vault_id, categories__pk=kwargs["pk"])
        return Response(
            data=NoteSerializer(qs, many=True, context={"request": request}).data
        )


class VaultViewSet(viewsets.BaseModelViewSet):
    queryset = Vault.objects.all()
    serializer_class = VaultSerializer
    permission_classes = [VaultOwnPermission]

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = drf_settings.DEFAULT_PERMISSION_CLASSES
            return [permission() for permission in self.permission_classes]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs

    @action(detail=True, methods=["get"], url_path="search-note")
    def search_note(self, request, *args, **kwargs):
        query = request.GET.get("query")
        qs = Note.objects.filter(folder__vault_id=kwargs["pk"])
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(categories__title__icontains=query)
            )
        return Response(
            data=NoteSerializer(qs, many=True, context={"request": request}).data
        )


class FolderViewSet(viewsets.BaseModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [VaultAndFolderOwnPermission]

    def get_permissions(self):
        if self.action in ["create", "list"]:
            self.permission_classes = [VaultOwnPermission]
            return [permission() for permission in self.permission_classes]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        vault_id = self.kwargs["vault_pk"]
        qs = qs.filter(vault_id=vault_id, vault__user=self.request.user)
        return qs

    def perform_create(self, serializer) -> None:
        vault = get_object_or_404(Vault, pk=self.kwargs["vault_pk"])
        serializer.save(vault=vault)


class NoteViewSet(viewsets.BaseModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [VaultAndFolderOwnPermission]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "update":
            return NoteUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        vault_id = self.kwargs["vault_pk"]
        qs = qs.filter(folder__vault_id=vault_id)
        if (type := self.request.GET.get("type")) and (
            type
            in [
                Note.SCRATCHPAD_NOTE_CHOICE,
                Note.FAVOURITE_NOTE_CHOICE,
                Note.TRASH_NOTE_CHOICE,
            ]
        ):
            # if there is type send all type's note from vault
            qs = qs.filter(type=type)
        else:
            folder_id = self.kwargs["folder_pk"]
            qs = qs.filter(folder_id=folder_id)
        return qs

    def perform_create(self, serializer) -> None:
        folder = get_object_or_404(Folder, pk=self.kwargs["folder_pk"])
        serializer.save(folder=folder)
