from django.conf import settings
from django.core.files.storage import Storage

from summers_api.trakt.utils import upload_to_imgur


class CustomFileStorage(Storage):
    def _open(self, name, mode="rb"):
        return None

    def _save(self, name, content):
        content_type = content.content_type
        if content_type in settings.IMGUR_SUPPORTED_FORMAT:
            file_url = upload_to_imgur(content)
            if file_url:
                return file_url
        # TODO(summer): upload somewhere else

    def exists(self, name):
        return False

    def url(self, name):
        return name
