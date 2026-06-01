import os
import shutil
import tempfile

import gdown

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def get_youtube_service():

    credentials = Credentials(
        token=None,
        refresh_token=os.getenv(
            "YOUTUBE_REFRESH_TOKEN"
        ),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv(
            "YOUTUBE_CLIENT_ID"
        ),
        client_secret=os.getenv(
            "YOUTUBE_CLIENT_SECRET"
        )
    )

    credentials.refresh(
        Request()
    )

    youtube = build(
        "youtube",
        "v3",
        credentials=credentials
    )

    return youtube


def upload_to_youtube(
    video_link: str,
    metadata: dict
) -> str:

    youtube = get_youtube_service()

    temp_dir = tempfile.mkdtemp()

    try:

        video_path = os.path.join(
            temp_dir,
            "video.mp4"
        )

        print(
            "Downloading video..."
        )

        gdown.download(
            video_link,
            video_path,
            fuzzy=True,
            quiet=False
        )

        title = metadata.get(
            "title",
            ""
        )

        description = metadata.get(
            "description",
            ""
        )

        hashtags = metadata.get(
            "hashtags",
            ""
        )

        tags = metadata.get(
            "tags",
            []
        )

        full_description = (
            description
            + "\n\n"
            + hashtags
        )

        print(
            "Uploading to YouTube..."
        )

        request = youtube.videos().insert(

            part="snippet,status",

            body={

                "snippet": {

                    "title":
                        title,

                    "description":
                        full_description,

                    "tags":
                        tags,

                    "categoryId":
                        "27"
                },

                "status": {

                    "privacyStatus":
                        "public",

                    "selfDeclaredMadeForKids":
                        False
                }
            },

            media_body=MediaFileUpload(
                video_path,
                resumable=True
            )
        )

        response = None

        while response is None:

            status, response = (
                request.next_chunk()
            )

            if status:

                progress = int(
                    status.progress() * 100
                )

                print(
                    f"Upload Progress: "
                    f"{progress}%"
                )

        video_id = response["id"]

        print(
            f"Upload Complete: "
            f"{video_id}"
        )

        return video_id

    finally:

        shutil.rmtree(
            temp_dir,
            ignore_errors=True
        )
