import os
import json
import re

import google.generativeai as genai


genai.configure(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


MASTER_PROMPT = """

You are a world-class viral content strategist specializing in:

* Threads

Your objective is to generate metadata that maximizes:

* Engagement
* Replies
* Reposts
* Shares
* Discussion
* Reach

---

## STEP 1: CONTENT ANALYSIS

Analyze the transcript and identify:

1. Primary Topic
2. Target Audience
3. Emotional Trigger

Choose ONE dominant emotion:

* Curiosity
* Shock
* Inspiration
* Fear
* Happiness
* Nostalgia
* Motivation
* Surprise
* Sadness
* Humor
* Cute Factor
* Satisfaction

4. Viral Angle

Determine why someone would stop scrolling.

Examples:

* Unexpected twist
* Hidden fact
* Emotional moment
* Cute interaction
* Transformation
* Life lesson
* Rare footage
* Funny situation
* Mind-blowing reveal

5. Content Category

Choose:

* Story
* Motivation
* Life Lesson
* Talking Objects
* Talking Food
* Facts
* Animals
* AI Content
* Relationship
* Humor
* Inspirational
* Educational
* Mystery
* History
* Finance
* Business
* Productivity

---

## PLATFORM STRATEGY

Threads content should:

✓ Feel human
✓ Encourage discussion
✓ Sound conversational
✓ Create curiosity
✓ Encourage replies
✓ Avoid sounding like an ad
✓ Avoid sounding AI-generated

---

## OUTPUT

Return ONLY valid JSON.

{
  "analysis": {
    "primary_topic": "",
    "target_audience": "",
    "emotion": "",
    "viral_angle": "",
    "content_category": ""
  },

  "thread_text": "",

  "question": "",

  "hashtags": []
}

Rules:

- thread_text must be under 450 characters
- Start with a strong hook
- Use short paragraphs
- Sound natural
- Do not use excessive emojis
- End with curiosity or discussion
- question should encourage comments
- Generate 5-10 relevant hashtags

---

TRANSCRIPT

{ocr_text}

"""


def extract_json(text):

    match = re.search(
        r"\{.*\}",
        text,
        re.DOTALL
    )

    if not match:
        raise ValueError(
            "No JSON found in response"
        )

    return json.loads(
        match.group()
    )


def generate_threads_metadata(
    ocr_text
):

    prompt = MASTER_PROMPT.format(
        ocr_text=ocr_text
    )

    response = model.generate_content(
        prompt
    )

    metadata = extract_json(
        response.text
    )

    return metadata