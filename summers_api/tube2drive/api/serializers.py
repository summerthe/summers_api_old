from django.contrib.auth import get_user_model
from rest_framework import serializers

from summers_api.tube2drive.models import UploadRequest

User = get_user_model()


class UploadRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadRequest
        fields = ("playlist_id", "folder_id")
        read_only_fields = ("user",)

    def save(self, **kwargs):
        request = self.context.get("request")
        user = request.user
        return super().save(user=user)
