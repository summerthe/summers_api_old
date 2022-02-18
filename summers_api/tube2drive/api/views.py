from django.contrib.auth import get_user_model

from base.apis import viewsets
from summers_api.tube2drive.api.serializers import UploadRequestSerializer
from summers_api.tube2drive.models import UploadRequest

User = get_user_model()


class UploadRequestViewSet(viewsets.BaseCreateListRetrieveModelViewSet):
    """
    Following Endpoints are created by this modelviewset.

    Create: POST `/`
    List: GET `/`
    Retrieve: GET `/<pk>/`
    """

    queryset = UploadRequest.objects.all()
    serializer_class = UploadRequestSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs
