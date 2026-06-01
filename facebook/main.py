import json
from datetime import datetime

from facebook_upload import upload_to_facebook
from generate_meta_data import generate_facebook_metadata

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

    for video in videos:

        facebook_data = video[
            "platforms"
        ]["facebook"]

        if not facebook_data[
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

    # =====================================
    # STEP 1: OCR
    # =====================================

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

    # =====================================
    # STEP 2: FACEBOOK METADATA
    # =====================================

    facebook_data = video[
        "platforms"
    ]["facebook"]

    metadata = facebook_data.get(
        "metadata",
        {}
    )

    if not metadata:

        print(
            "Generating Facebook metadata..."
        )

        metadata = (
            generate_facebook_metadata(
                ocr_text
            )
        )

        facebook_data[
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

    # =====================================
    # STEP 3: UPLOAD TO FACEBOOK
    # =====================================

    print(
        "Uploading video to Facebook..."
    )

    upload_id = upload_to_facebook(
        video_link=video["video"][
            "drive_link"
        ],
        metadata=metadata
    )

    # =====================================
    # STEP 4: UPDATE JSON
    # =====================================

    facebook_data[
        "uploaded"
    ] = True

    facebook_data[
        "upload_id"
    ] = upload_id

    facebook_data[
        "uploaded_at"
    ] = (
        datetime.utcnow()
        .isoformat()
    )

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
        f"Facebook Upload ID: "
        f"{upload_id}"
    )


if __name__ == "__main__":
    main()