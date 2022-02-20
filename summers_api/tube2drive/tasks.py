from tube2drive.utils import find_playlist_and_upload


def run_find_playlist_and_upload(
    playlist_id: str,
    folder_id: str,
    upload_request_id: int,
) -> None:
    find_playlist_and_upload(
        playlist_id,
        folder_id,
        upload_request_id,
    )
