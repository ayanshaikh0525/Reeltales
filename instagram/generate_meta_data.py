import os
import json
import re

import google.generativeai as genai


genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)


model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


MASTER_PROMPT = """
You are a world-class viral content strategist specializing in Instagram Reels.

Your objective is to maximize:

- Shares
- Saves
- Comments
- Watch Time
- Replays

Analyze the transcript and generate viral Instagram metadata.

TRANSCRIPT:

{ocr_text}

RETURN ONLY VALID JSON.

{
  "viral_analysis": {
    "primary_topic": "",
    "target_audience": "",
    "emotion": "",
    "viral_angle": "",
    "content_category": ""
  },

  "caption": "",

  "hooks": [
    "",
    "",
    "",
    "",
    ""
  ],

  "hashtags": [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    ""
  ]
}
"""

def generate_instagram_metadata(
    ocr_text: str
):
    prompt = MASTER_PROMPT.format(
        ocr_text=ocr_text
    )

    response = model.generate_content(
        prompt
    )

    content = response.text.strip()

    content = re.sub(
        r"^```json",
        "",
        content
    )

    content = re.sub(
        r"```$",
        "",
        content
    )

    content = content.strip()

    try:
        metadata = json.loads(
            content
        )

        return metadata

    except Exception as e:

        print(content)

        raise Exception(
            f"Failed to parse Instagram metadata: {e}"
        )