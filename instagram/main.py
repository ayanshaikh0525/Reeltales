import json
from datetime import datetime

from instagram_upload import upload_to_instagram
from generate_meta_data import generate_instagram_metadata

import sys
import os

ROOT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
sys.path.append(ROOT_DIR)

from process_video import generate_ocr_from_video


MASTER_JSON = "../master_videos.json"


def load_json():
    with open(
        MASTER_JSON,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def save_json(data):
    with open(
        MASTER_JSON,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def get_next_video(videos):
    """
    Returns first video
    not uploaded to Instagram.
    """

    for video in videos:

        instagram_data = (
            video["platforms"]
            ["instagram"]
        )

        if not instagram_data[
            "uploaded"
        ]:
            return video

    return None


def main():

    print(
        "Loading master_videos.json..."
    )

    videos = load_json()

    video = get_next_video(
        videos
    )

    if video is None:

        print(
            "No videos pending upload."
        )

        return

    print(
        f"Selected Video: "
        f"{video['video']['filename']}"
    )

    # ==========================
    # STEP 1: OCR
    # ==========================

    ocr_text = video[
        "content"
    ].get(
        "ocr_text",
        ""
    )

    if not ocr_text:

        print(
            "OCR text not found. "
            "Generating OCR..."
        )

        ocr_text = (
            generate_ocr_from_video(
                video["video"][
                    "drive_link"
                ]
            )
        )

        video["content"][
            "ocr_text"
        ] = ocr_text

        video["content"][
            "ocr_generated_at"
        ] = (
            datetime.utcnow()
            .isoformat()
        )

        save_json(videos)

        print(
            "OCR generated and saved."
        )

    else:

        print(
            "OCR already exists."
        )

    # ==========================
    # STEP 2: INSTAGRAM METADATA
    # ==========================

    instagram_data = (
        video["platforms"]
        ["instagram"]
    )

    metadata = (
        instagram_data.get(
            "metadata",
            {}
        )
    )

    if (
        not metadata
        or not metadata.get(
            "caption"
        )
    ):

        print(
            "Generating Instagram metadata..."
        )

        metadata = (
            generate_instagram_metadata(
                ocr_text
            )
        )

        instagram_data[
            "metadata"
        ] = metadata

        save_json(videos)

        print(
            "Metadata generated and saved."
        )

    else:

        print(
            "Metadata already exists."
        )

    # ==========================
    # STEP 3: UPLOAD INSTAGRAM
    # ==========================

    print(
        "Uploading video to Instagram..."
    )

    upload_id = (
        upload_to_instagram(
            video_link=video[
                "video"
            ][
                "drive_link"
            ],
            metadata=metadata
        )
    )

    # ==========================
    # STEP 4: UPDATE JSON
    # ==========================

    instagram_data[
        "uploaded"
    ] = True

    instagram_data[
        "upload_id"
    ] = upload_id

    instagram_data[
        "uploaded_at"
    ] = (
        datetime.utcnow()
        .isoformat()
    )

    video["content"][
        "processed"
    ] = True

    video["workflow"][
        "updated_at"
    ] = (
        datetime.utcnow()
        .isoformat()
    )

    save_json(videos)

    print(
        f"Successfully uploaded "
        f"{video['video']['filename']}"
    )

    print(
        f"Instagram Media ID: "
        f"{upload_id}"
    )


if __name__ == "__main__":
    main()