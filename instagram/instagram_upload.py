import requests
import time


class InstagramUploader:
    def __init__(
        self,
        access_token: str,
        instagram_account_id: str,
    ):
        self.access_token = access_token
        self.instagram_account_id = instagram_account_id

    def upload_reel(
        self,
        video_url: str,
        metadata: dict,
    ):
        caption = (
            metadata.get("description", "")
            + "\n\n"
            + " ".join(
                f"#{tag}"
                for tag in metadata.get("hashtags", [])
            )
        )

        create_url = (
            f"https://graph.facebook.com/v23.0/"
            f"{self.instagram_account_id}/media"
        )

        create_payload = {
            "media_type": "REELS",
            "video_url": video_url,
            "caption": caption,
            "access_token": self.access_token,
        }

        response = requests.post(
            create_url,
            data=create_payload,
        )

        response.raise_for_status()

        creation_id = response.json()["id"]

        status_url = (
            f"https://graph.facebook.com/v23.0/"
            f"{creation_id}"
        )

        while True:
            status_response = requests.get(
                status_url,
                params={
                    "fields": "status_code",
                    "access_token": self.access_token,
                },
            )

            status_response.raise_for_status()

            status = status_response.json()["status_code"]

            print(f"Instagram Status: {status}")

            if status == "FINISHED":
                break

            if status == "ERROR":
                raise Exception(
                    "Instagram processing failed"
                )

            time.sleep(10)

        publish_url = (
            f"https://graph.facebook.com/v23.0/"
            f"{self.instagram_account_id}/media_publish"
        )

        publish_response = requests.post(
            publish_url,
            data={
                "creation_id": creation_id,
                "access_token": self.access_token,
            },
        )

        publish_response.raise_for_status()

        return publish_response.json()