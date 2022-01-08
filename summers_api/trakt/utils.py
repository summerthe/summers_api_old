import json

import requests
from django.conf import settings
from django.core.files import File


def upload_to_imgur(thumbnail):
    file_in_bytes = File(thumbnail).read()
    data = {"image": file_in_bytes}
    headers = {"Authorization": f"Client-ID {settings.IMGUR_CLIENT_ID}"}
    response = requests.post(
        settings.IMGUR_UPLOAD_ENDPOINT,
        data=data,
        headers=headers,
    )
    if response.status_code == 200:
        return json.loads(response.content.decode()).get("data").get("link")
