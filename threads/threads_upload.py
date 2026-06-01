import os
import requests


ACCESS_TOKEN = os.getenv(
    "THREADS_ACCESS_TOKEN"
)

USER_ID = os.getenv(
    "THREADS_USER_ID"
)


def upload_to_threads(
    metadata: dict
):
    """
    Creates and publishes
    a Threads text post.

    Returns:
        Published Thread ID
    """

    thread_text = (
        metadata["thread_text"]
        + "\n\n"
        + metadata["question"]
        + "\n\n"
        + " ".join(
            metadata["hashtags"]
        )
    )

    # ==========================
    # STEP 1:
    # CREATE THREAD CONTAINER
    # ==========================

    create_url = (
        f"https://graph.threads.net/v1.0/"
        f"{USER_ID}/threads"
    )

    create_payload = {
        "media_type": "TEXT",
        "text": thread_text,
        "access_token": ACCESS_TOKEN
    }

    create_response = requests.post(
        create_url,
        data=create_payload,
        timeout=60
    )

    create_response.raise_for_status()

    create_data = (
        create_response.json()
    )

    creation_id = create_data["id"]

    print(
        f"Thread container created: "
        f"{creation_id}"
    )

    # ==========================
    # STEP 2:
    # PUBLISH THREAD
    # ==========================

    publish_url = (
        f"https://graph.threads.net/v1.0/"
        f"{USER_ID}/threads_publish"
    )

    publish_payload = {
        "creation_id": creation_id,
        "access_token": ACCESS_TOKEN
    }

    publish_response = requests.post(
        publish_url,
        data=publish_payload,
        timeout=60
    )

    publish_response.raise_for_status()

    publish_data = (
        publish_response.json()
    )

    thread_id = publish_data["id"]

    print(
        f"Thread published: "
        f"{thread_id}"
    )

    return thread_id