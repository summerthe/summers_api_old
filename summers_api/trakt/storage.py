import json

import requests
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage


class ImgurFileStorage(Storage):
    def _open(self, name, mode="rb"):
        return None

    def _save(self, name, content):
        self.file_url = upload_to_imgur(content)
        return self.file_url

    def exists(self, name):
        return False

    def url(self, name):
        return name


def upload_to_imgur(thumbnail):
    file_in_bytes = File(thumbnail).read()
    data = {"image": file_in_bytes}
    headers = {"Authorization": f"Client-ID {settings.IMGUR_CLIENT_ID}"}
    response = requests.post(
        "https://api.imgur.com/3/image/",
        data=data,
        headers=headers,
    )
    if response.status_code == 200:
        return json.loads(response.content.decode()).get("data").get("link")
