from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework.response import Response

from base.apis import viewsets
from base.apis.permissions import AppOwnPermission
from summers_api.tube2drive.api.serializers import (
    UploadRequestSerializer,
    UploadRequestUpdateStatusSerializer,
)
from summers_api.tube2drive.models import UploadRequest

User = get_user_model()


class UploadRequestViewSet(viewsets.BaseCreateListRetrieveUpdateModelViewSet):
    """
    Following Endpoints are created by this modelviewset.

    Create: POST `/`
    List: GET `/`
    Retrieve: GET `/<pk>/`
    """

    queryset = UploadRequest.objects.all()
    serializer_class = UploadRequestSerializer

    def get_permissions(self):
        if self.action == "update":
            return [AppOwnPermission()]
        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        if isinstance(self.request.user, AnonymousUser):
            return qs
        qs = qs.filter(user=self.request.user)
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = UploadRequestUpdateStatusSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(UploadRequestSerializer(instance).data)
