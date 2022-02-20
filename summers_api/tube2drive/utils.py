import json
import multiprocessing
import os
import time
import traceback
from typing import List

import googleapiclient
import googleapiclient.discovery
import redis
import requests
import yt_dlp
from celery.execute import send_task
from django.conf import settings
from django.urls import reverse_lazy
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

from summers_api.tube2drive.models import UploadRequest


def find_playlist_and_upload(
    playlist_id: str,
    folder_id: str,
    upload_request_id: int,
) -> None:

    # upload_request = UploadRequest.objects.get(pk=upload_request_id)
    # request_status = UploadRequest.RUNNING_CHOICE
    # upload_request.status = request_status
    # upload_request.save()
    # hit upload api to update upload request status
    update_upload_request_status(upload_request_id, UploadRequest.RUNNING_CHOICE)
    try:
        videos = fetch_youtube_video_ids(playlist_id)
    except Exception:
        videos = []
        traceback.print_exc()

    if videos is None or len(videos) == 0:
        request_status = UploadRequest.NOT_FOUND_CHOICE
    else:
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

                try:
                    upload_to_drive(filename, folder_id)
                # except PermissionError:
                #   # request_status = UploadRequest.FAILED_CHOICE
                #   # break
                except Exception:
                    traceback.print_exc()
                finally:
                    os.remove(filename)

            except Exception:
                traceback.print_exc()

            counter += 1
        else:
            request_status = UploadRequest.COMPLETED_CHOICE

    # hit upload api to update upload request status
    update_upload_request_status(upload_request_id, request_status)


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


def check_task_to_find_playlist_and_upload(
    playlist_id: str,
    folder_id: str,
    upload_request_pk: int,
):
    # check if redis is runing
    try:
        redis_host = settings.REDIS_URL
        r = redis.Redis(
            redis_host, socket_connect_timeout=1  # short timeout for the test
        )
        r.ping()
        print("Redis is running")
        send_task(
            "tube2drive.tasks.run_find_playlist_and_upload",
            args=(
                playlist_id,
                folder_id,
                upload_request_pk,
            ),
        )
    except redis.exceptions.ConnectionError:
        print("Run process in backend")
        # else run in background
        # ping heroku on every 5 minutes so it dont turn off dyno

        run_upload_process(playlist_id, folder_id, upload_request_pk)


def run_upload_process(playlist_id: str, folder_id: str, upload_request_pk: int):
    main_proces = multiprocessing.Process(
        target=find_playlist_and_upload,
        args=(
            playlist_id,
            folder_id,
            upload_request_pk,
        ),
    )
    main_proces.start()

    while True:
        if main_proces.is_alive():
            time.sleep(300)
            print("Hitting Heroku")
            ping_heroku_server()
        else:
            break


def ping_heroku_server():
    hosts = settings.ALLOWED_HOSTS
    print("hosts", hosts)
    for host in filter(lambda k: "herokuapp.com" in k, hosts):
        requests.get(f"http://{host}")


def update_upload_request_status(pk, status):
    print(settings.CURRENT_DOMAIN, "CURRENT_DOMAIN")
    url = settings.CURRENT_DOMAIN + reverse_lazy(
        "api:summers_api.tube2drive:upload-requests-detail", kwargs={"pk": pk}
    )

    print("url", url)

    payload = json.dumps({"status": status})
    headers = {"App-Own": "", "Content-Type": "application/json"}

    requests.request("PUT", url, headers=headers, data=payload)
