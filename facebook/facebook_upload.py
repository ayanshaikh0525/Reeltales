import os
import requests


ACCESS_TOKEN = os.getenv(
    "FACEBOOK_ACCESS_TOKEN"
)

PAGE_ID = os.getenv(
    "FACEBOOK_PAGE_ID"
)


def upload_to_facebook(
    video_link: str,
    metadata: dict
):

    caption = metadata.get(
        "caption",
        ""
    )

    hashtags = metadata.get(
        "hashtags",
        ""
    )

    description = (
        f"{caption}\n\n"
        f"{hashtags}"
    )

    # =================================
    # STEP 1
    # CREATE REEL CONTAINER
    # =================================

    print(
        "Creating Facebook Reel..."
    )

    create_url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PAGE_ID}/video_reels"
    )

    create_payload = {
        "access_token": ACCESS_TOKEN,
        "video_url": video_link,
        "description": description
    }

    create_response = requests.post(
        create_url,
        data=create_payload,
        timeout=300
    )

    create_response.raise_for_status()

    create_data = (
        create_response.json()
    )

    video_id = create_data.get(
        "video_id"
    )

    if not video_id:

        raise Exception(
            f"Facebook creation failed: "
            f"{create_data}"
        )

    print(
        f"Facebook video created: "
        f"{video_id}"
    )

    # =================================
    # STEP 2
    # PUBLISH REEL
    # =================================

    publish_url = (
        f"https://graph.facebook.com/v23.0/"
        f"{PAGE_ID}/video_reels_publish"
    )

    publish_payload = {
        "access_token": ACCESS_TOKEN,
        "video_id": video_id
    }

    publish_response = requests.post(
        publish_url,
        data=publish_payload,
        timeout=300
    )

    publish_response.raise_for_status()

    publish_data = (
        publish_response.json()
    )

    print(
        "Facebook Reel published."
    )

    print(
        publish_data
    )

    return video_id