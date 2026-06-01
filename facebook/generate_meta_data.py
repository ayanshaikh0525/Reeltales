import os
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

* Facebook Reels

Your objective is to generate metadata that maximizes:

* Click Through Rate (CTR)
* Average Watch Duration
* Shares
* Saves
* Comments
* Rewatches
* Platform Distribution

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

## VIRAL COPYWRITING RULES

Generate copy using:

✓ Curiosity gaps
✓ Open loops
✓ Emotional tension
✓ High-retention wording
✓ Human conversational style
✓ Native platform language
✓ Short punchy phrases
✓ Scroll-stopping hooks

Avoid:

✗ Generic captions
✗ Clickbait that breaks trust
✗ Robotic wording
✗ Repetitive hooks
✗ Overused hashtags

---

## FACEBOOK REELS STRATEGY

Optimize for:

* Shares
* Community engagement
* Emotional connection

Create:

* 1 primary caption
* 20 hashtags
* 5 hook variations

---

## OUTPUT FORMAT

[VIRAL_ANALYSIS]

Primary Topic:
Target Audience:
Emotion:
Viral Angle:
Content Category:

[FACEBOOK_CAPTION]

[FACEBOOK_HASHTAGS]

[FACEBOOK_HOOKS]
1.
2.
3.
4.
5.

---

## TRANSCRIPT

{ocr_text}
"""


def extract_section(
    text,
    start_tag,
    end_tag=None
):

    if end_tag:

        pattern = (
            rf"\[{start_tag}\](.*?)"
            rf"\[{end_tag}\]"
        )

    else:

        pattern = (
            rf"\[{start_tag}\](.*)"
        )

    match = re.search(
        pattern,
        text,
        re.DOTALL
    )

    if match:
        return match.group(1).strip()

    return ""


def generate_facebook_metadata(
    ocr_text
):

    prompt = MASTER_PROMPT.format(
        ocr_text=ocr_text
    )

    response = model.generate_content(
        prompt
    )

    content = response.text.strip()

    caption = extract_section(
        content,
        "FACEBOOK_CAPTION",
        "FACEBOOK_HASHTAGS"
    )

    hashtags = extract_section(
        content,
        "FACEBOOK_HASHTAGS",
        "FACEBOOK_HOOKS"
    )

    hooks_section = extract_section(
        content,
        "FACEBOOK_HOOKS"
    )

    hooks = [
        line.strip("-•1234567890. ")
        for line in hooks_section.splitlines()
        if line.strip()
    ]

    return {
        "raw_response": content,
        "caption": caption,
        "hashtags": hashtags,
        "hooks": hooks
    }