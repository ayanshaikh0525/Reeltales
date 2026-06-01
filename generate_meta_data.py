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

  * YouTube Shorts

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

  ✗ Generic titles
  ✗ Clickbait that breaks trust
  ✗ Robotic SEO wording
  ✗ Repetitive hooks
  ✗ Overused hashtags

  ---

  ## PLATFORM-SPECIFIC STRATEGY

  YOUTUBE SHORTS

  Optimize for:

  * CTR
  * Search discovery
  * Suggested feed
  * Viewer retention

  Create:

  * 5 title variations
  * Mix curiosity + SEO
  * Thumbnail text under 4 words

  
  ---

  ## ADVANCED HASHTAG RULES

  Generate hashtags in 3 layers:

  Layer 1:
  Large audience hashtags

  Layer 2:
  Niche-specific hashtags

  Layer 3:
  Trend/viral hashtags

  Do NOT generate generic spam hashtags.

  ---

  ## SEO RULES

  Extract:

  * Primary keyword
  * Secondary keywords
  * Long-tail keywords

  Use naturally.

  ---

  ## OUTPUT FORMAT

  [VIRAL_ANALYSIS]

  Primary Topic:
  Target Audience:
  Emotion:
  Viral Angle:
  Content Category:

  [YOUTUBE_TITLES]
  5 Titles

  [YOUTUBE_DESCRIPTION]

  [YOUTUBE_HASHTAGS]
  20 Hashtags

  [YOUTUBE_KEYWORDS]


  [BONUS_CTA]
  3 Strong CTAs

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
