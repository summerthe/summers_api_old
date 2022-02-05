from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

from base.apis import viewsets
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

    @action(detail=True, methods=["get"], url_path="notes")
    def note(self, request, *args, **kwargs):
        vault_id = request.GET.get("vault_id")
        qs = Note.objects.filter(folder__vault_id=vault_id, categories__pk=kwargs["pk"])
        return Response(
            data=NoteSerializer(qs, many=True, context={"request": request}).data
        )


class VaultViewSet(viewsets.BaseModelViewSet):
    queryset = Vault.objects.all()
    serializer_class = VaultSerializer

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

    def get_queryset(self):
        qs = super().get_queryset()
        vault_id = self.kwargs["vault_pk"]
        qs = qs.filter(vault_id=vault_id)
        return qs

    def perform_create(self, serializer) -> None:
        vault = get_object_or_404(Vault, pk=self.kwargs["vault_pk"])
        serializer.save(vault=vault)


class NoteViewSet(viewsets.BaseModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "update":
            return NoteUpdateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        folder_id = self.kwargs["folder_pk"]
        qs = qs.filter(folder_id=folder_id)
        return qs

    def perform_create(self, serializer) -> None:
        folder = get_object_or_404(Folder, pk=self.kwargs["folder_pk"])
        serializer.save(folder=folder)
