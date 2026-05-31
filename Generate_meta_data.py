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


def generate_youtube_metadata(
    ocr_text
):

    prompt = MASTER_PROMPT.format(
        ocr_text=ocr_text
    )

    response = model.generate_content(
        prompt
    )

    content = response.text.strip()

    titles_section = extract_section(
        content,
        "YOUTUBE_TITLES",
        "YOUTUBE_DESCRIPTION"
    )

    description = extract_section(
        content,
        "YOUTUBE_DESCRIPTION",
        "YOUTUBE_HASHTAGS"
    )

    hashtags = extract_section(
        content,
        "YOUTUBE_HASHTAGS",
        "YOUTUBE_KEYWORDS"
    )

    keywords = extract_section(
        content,
        "YOUTUBE_KEYWORDS",
        "BONUS_CTA"
    )

    titles = [
        line.strip("-•1234567890. ")
        for line in titles_section.splitlines()
        if line.strip()
    ]

    title = (
        titles[0]
        if titles
        else "Untitled Video"
    )

    return {
        "raw_response": content,
        "title": title,
        "description": description,
        "hashtags": hashtags,
        "keywords": keywords
    }
