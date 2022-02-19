import os
import traceback
from typing import List

import googleapiclient
import googleapiclient.discovery
import yt_dlp
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload


def find_playlist_and_upload(playlist_id: str, folder_id: str) -> None:

    videos = fetch_youtube_video_ids(playlist_id)

    if not videos:
        return

    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    youtube_api_service_name = "youtube"
    youtube_api_version = "v3"

    credentials = service_account.Credentials.from_service_account_info(
        settings.GCP_SERVICE_ACCOUNT_JSON,
        scopes=scopes,
    )
    youtube_client = googleapiclient.discovery.build(
        youtube_api_service_name,
        youtube_api_version,
        credentials=credentials,
        cache_discovery=False,
    )

    counter = 1
    for video in videos:
        request = youtube_client.videos().list(part="snippet", id=video)
        response = request.execute()
        filename = "{}-{}".format(counter, response["items"][0]["snippet"]["title"])
        filename = filename.replace("%", "per")
        ydl_opts = {"outtmpl": filename}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(["https://www.youtube.com/watch?v={}".format(video)])

            if not os.path.exists(filename):
                filename += ".webm"

            upload_to_drive(filename, folder_id)
        except Exception:
            traceback.print_exc()

        counter += 1


def fetch_youtube_video_ids(playlist_id: str) -> List[str]:
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    youtube_api_service_name = "youtube"
    youtube_api_version = "v3"

    credentials = service_account.Credentials.from_service_account_info(
        settings.GCP_SERVICE_ACCOUNT_JSON,
        scopes=scopes,
    )
    youtube_client = googleapiclient.discovery.build(
        youtube_api_service_name,
        youtube_api_version,
        credentials=credentials,
        cache_discovery=False,
    )

    responses = []

    request = youtube_client.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
    )
    response = request.execute()
    responses.append(response)

    # All video's id
    video_ids = []

    # for first page
    try:
        for item in response["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
    except Exception:
        traceback.print_exc()

    # iterating over pagination and fetching all video_ids
    try:
        while True:
            request = youtube_client.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                pageToken=response["nextPageToken"],
            )
            response = request.execute()

            for item in response["items"]:
                try:
                    video_ids.append(item["snippet"]["resourceId"]["videoId"])
                except Exception:
                    traceback.print_exc()
    except Exception:
        traceback.print_exc()

    return video_ids


def upload_to_drive(
    filename: str,
    folder_id: str,
) -> None:
    # Call the Drive v3 API
    # create folder in your account and share that folder with service account
    # so service account can create file in that folder.
    scopes = ["https://www.googleapis.com/auth/drive"]
    drive_api_service_name = "drive"
    drive_api_version = "v3"

    credentials = service_account.Credentials.from_service_account_info(
        settings.GCP_SERVICE_ACCOUNT_JSON,
        scopes=scopes,
    )

    drive_client = googleapiclient.discovery.build(
        drive_api_service_name,
        drive_api_version,
        credentials=credentials,
        cache_discovery=False,
    )

    file_metadata = {"name": filename, "parents": [folder_id]}
    media = MediaFileUpload(filename, mimetype="video/*")

    drive_client.files().create(
        body=file_metadata, media_body=media, fields="id"
    ).execute()

    os.remove(filename)
