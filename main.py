import json
from datetime import datetime

from process_video import generate_ocr_from_video
from youtube_upload import upload_to_youtube
from Generate_meta_data import generate_youtube_metadata


MASTER_JSON = "master_videos.json"


def load_json():
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data):
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def get_next_video(videos):
    """
    Returns the first video that has not
    been uploaded to YouTube.
    """

    for video in videos:

        youtube_data = video["platforms"]["youtube"]

        if not youtube_data["uploaded"]:
            return video

    return None


def main():

    print("Loading master_videos.json...")

    videos = load_json()

    video = get_next_video(videos)

    if video is None:
        print("No videos pending upload.")
        return

    print(
        f"Selected Video: "
        f"{video['video']['filename']}"
    )

    # =====================================
    # STEP 1: OCR
    # =====================================

    ocr_text = video["content"].get(
        "ocr_text",
        ""
    )

    if not ocr_text:

        print(
            "OCR text not found. "
            "Generating OCR..."
        )

        ocr_text = generate_ocr_from_video(
            video["video"]["drive_link"]
        )

        video["content"]["ocr_text"] = (
            ocr_text
        )

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
    # STEP 2: YOUTUBE METADATA
    # =====================================

    youtube_data = video["platforms"][
        "youtube"
    ]

    metadata = youtube_data.get(
        "metadata",
        {}
    )

    if (
        not metadata
        or not metadata.get("title")
    ):

        print(
            "Generating YouTube metadata..."
        )

        metadata = (
            generate_youtube_metadata(
                ocr_text
            )
        )

        youtube_data["metadata"] = (
            metadata
        )

        save_json(videos)

        print(
            "Metadata generated and saved."
        )

    else:

        print(
            "Metadata already exists."
        )

    # =====================================
    # STEP 3: UPLOAD TO YOUTUBE
    # =====================================

    print(
        "Uploading video to YouTube..."
    )

    upload_id = upload_to_youtube(
        video_link=video["video"][
            "drive_link"
        ],
        metadata=metadata
    )

    # =====================================
    # STEP 4: UPDATE JSON
    # =====================================

    youtube_data["uploaded"] = True

    youtube_data["upload_id"] = (
        upload_id
    )

    youtube_data["uploaded_at"] = (
        datetime.utcnow()
        .isoformat()
    )

    video["content"]["processed"] = (
        True
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
        f"YouTube Video ID: "
        f"{upload_id}"
    )


if __name__ == "__main__":
    main()
