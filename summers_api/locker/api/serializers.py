from django.contrib.auth import get_user_model
from rest_framework import serializers

from summers_api.locker.models import Category, Folder, Note, Vault

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("user",)

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user
        return super().save(user=user)


class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = "__all__"
        read_only_fields = ("user",)

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user
        return super().save(user=user)


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"
        read_only_fields = ("vault",)


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("folder",)


class NoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ("folder",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
