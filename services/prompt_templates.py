"""
Prompt Engineering Module for AI Content Studio.

This module is the core of the prompt engineering architecture.
It dynamically constructs structured, context-aware prompts for Google Gemini
by combining role-definition, task specification, domain-specific requirements,
audience targeting, tone, length constraints, writing style, and user guidelines.
"""

from typing import Dict, Optional

# Content-specific prompt engineering templates and requirements
BLOG_REQUIREMENTS = """
Blog Post Specific Guidelines:
- Title: Generate an attention-grabbing, SEO-optimized title at the very beginning.
- Structure: Include an engaging introductory hook, well-structured subheadings (use Markdown ## and ###), and concise paragraphs.
- Body: Provide informative, well-researched insights, actionable takeaways, and concrete real-world examples or analogies where appropriate.
- Conclusion: End with a cohesive conclusion summarizing key points and leaving the reader with a thought-provoking closing thought.
""".strip()

LINKEDIN_REQUIREMENTS = """
LinkedIn Post Specific Guidelines:
- Hook: Start with a powerful 1-2 line opening hook that stops the scroll.
- Tone & Format: Professional yet personal, authentic, and insight-driven. Use short sentences, 1-2 line micro-paragraphs, and bullet points for maximum mobile readability.
- Value Delivery: Share a practical lesson, industry insight, or perspective that adds clear value to professionals.
- Call to Action: End with an engaging open-ended question to spark discussion in the comments section.
- Hashtags: Include 3 to 5 targeted, high-relevance hashtags at the very bottom.
""".strip()

SOCIAL_REQUIREMENTS = """
Social Media Caption Specific Guidelines:
- Opening: Create a snappy, attention-grabbing opening line with personality.
- Formatting: Keep it punchy, visually clean, and easy to skim. Use relevant emojis naturally to accentuate points without overdoing it.
- Engagement: Include an interactive call to action (e.g., "Drop your thoughts below 👇" or "Save this for later!").
- Hashtags: Append 4 to 8 popular and relevant hashtags grouped cleanly at the end.
""".strip()

EMAIL_REQUIREMENTS = """
Email Specific Guidelines:
- Subject Line: Provide 2-3 compelling, high-open-rate subject line options (e.g., Direct, Curiosity-driven).
- Greeting: Include a professional and context-appropriate greeting (e.g., "Hi [Name]," or "Dear [Team/Client],").
- Body: Deliver the core message clearly and concisely, respecting the recipient's time. Use bullet points if listing key points or benefits.
- Call to Action (CTA): Clearly articulate the desired next step with an unambiguous CTA.
- Sign-off: Conclude with a warm, professional closing and placeholder signature.
""".strip()

PRODUCT_REQUIREMENTS = """
Product Description Specific Guidelines:
- Headline: A captivating headline that immediately conveys the product's primary value proposition.
- Hook: Clearly identify the target customer's pain point and how the product solves it.
- Key Features & Benefits: Highlight 3-5 standout features, explicitly explaining the practical benefit of each (Feature -> Benefit).
- Specifications & Use Cases: Provide clear use case scenarios and practical details.
- Call to Action: Finish with a compelling, conversion-focused closing (e.g., "Upgrade your workflow today").
""".strip()

AD_REQUIREMENTS = """
Advertisement Copy Specific Guidelines:
- Headlines: Generate 3 high-converting headline variations (Value-Focused, Problem-Solver, Curiosity).
- Hook & Core Copy: Craft persuasive copy emphasizing the Unique Value Proposition (UVP), addressing potential objections, and creating urgency or desire.
- Social Proof / Trust: Include a brief line or trigger establishing credibility.
- Call to Action (CTA): Deliver a punchy, direct CTA button/action text (e.g., "Get Started Free", "Claim Your Offer").
""".strip()

YOUTUBE_REQUIREMENTS = """
YouTube Description Specific Guidelines:
- Video Title: Provide 2-3 click-worthy, SEO-rich video title suggestions.
- Overview: A compelling 2-3 paragraph summary of what viewers will learn and why they should watch.
- Timestamps: Provide sample video chapter breakdown placeholders (e.g., 00:00 - Introduction, 01:15 - Key Concept, 04:30 - Deep Dive, 07:45 - Summary & Wrap Up).
- Links & Resources: Include formatted placeholders for relevant links, social channels, and resources.
- Tags & Keywords: Provide 8-12 search-optimized keywords and video hashtags.
""".strip()

STORY_REQUIREMENTS = """
Creative Story Specific Guidelines:
- Title: An evocative and thematic story title.
- Narrative Arc: Establish an engaging setting, introduce relatable characters, introduce a central conflict or dilemma, build tension, and conclude with a satisfying resolution or twist.
- Style: Use vivid sensory imagery, dynamic pacing, and realistic dialogue where appropriate. Show, don't just tell.
""".strip()

CUSTOM_REQUIREMENTS = """
Custom Content Specific Guidelines:
- Adapt dynamically to the user's specific guidelines and context.
- Maintain exceptional structural clarity, crisp readability, and appropriate formatting (headings, bullet points, emphasis).
- Ensure the output strictly addresses the requested goals and audience.
""".strip()

# Mapping of content types to their specific requirements
CONTENT_TYPE_RULES: Dict[str, str] = {
    "Blog Post": BLOG_REQUIREMENTS,
    "LinkedIn Post": LINKEDIN_REQUIREMENTS,
    "Social Media Caption": SOCIAL_REQUIREMENTS,
    "Email": EMAIL_REQUIREMENTS,
    "Product Description": PRODUCT_REQUIREMENTS,
    "Advertisement Copy": AD_REQUIREMENTS,
    "YouTube Description": YOUTUBE_REQUIREMENTS,
    "Creative Story": STORY_REQUIREMENTS,
    "Custom Content": CUSTOM_REQUIREMENTS,
}

# Mapping of length constraints based on content type
LENGTH_GUIDELINES: Dict[str, Dict[str, str]] = {
    "Short": {
        "default": "Approximately 150 - 250 words. Focus on brevity, punchy phrasing, and high-density information.",
        "Social Media Caption": "Approximately 50 - 100 words. Keep it very concise and punchy.",
        "Advertisement Copy": "Approximately 50 - 100 words. High impact, minimal words.",
        "Email": "Approximately 100 - 180 words. Direct and quick to read.",
    },
    "Medium": {
        "default": "Approximately 400 - 600 words. Deliver thorough coverage with balanced depth and clear structure.",
        "Social Media Caption": "Approximately 120 - 200 words. More storytelling or detailed tips.",
        "Advertisement Copy": "Approximately 120 - 200 words. Extended value proposition with objection handling.",
        "Email": "Approximately 200 - 350 words. Detailed proposal, newsletter, or announcement.",
    },
    "Long": {
        "default": "Approximately 800 - 1200 words. Comprehensive, deeply detailed exploration with extensive insights.",
        "Social Media Caption": "Approximately 250 - 350 words. Micro-blog style caption.",
        "Advertisement Copy": "Approximately 250 - 400 words. Long-form sales letter or landing page copy.",
        "Email": "Approximately 400 - 600 words. Comprehensive email newsletter or long-form nurture email.",
    }
}

# Role definitions for expert persona prompting
ROLE_DEFINITIONS: Dict[str, str] = {
    "Creative Story": "an award-winning creative author and master storyteller",
    "Advertisement Copy": "a world-class direct-response advertising copywriter and marketing strategist",
    "LinkedIn Post": "an influential executive thought leader and professional brand strategist",
    "Blog Post": "a seasoned content marketing lead and authoritative technical/editorial writer",
    "Email": "an expert email marketing strategist and persuasive corporate communicator",
    "Product Description": "a premier e-commerce conversion strategist and product marketing specialist",
    "YouTube Description": "a top-tier YouTube growth consultant and digital video SEO strategist",
    "Social Media Caption": "a viral social media strategist and digital community architect",
    "Custom Content": "an expert content strategist and versatile professional writer",
}


def get_supported_content_types() -> list:
    """Return list of supported content types."""
    return list(CONTENT_TYPE_RULES.keys())


def build_prompt(
    content_type: str,
    topic: str,
    audience: Optional[str] = "General Audience",
    tone: Optional[str] = "Professional",
    length: Optional[str] = "Medium",
    style: Optional[str] = "Conversational",
    additional_instructions: Optional[str] = None
) -> str:
    """
    Construct a comprehensive, context-aware prompt for Google Gemini.

    Parameters:
        content_type: Selected format (e.g. 'Blog Post', 'LinkedIn Post')
        topic: User's primary topic or context description
        audience: Intended target demographic
        tone: Desired voice (e.g. 'Professional', 'Persuasive')
        length: Target length ('Short', 'Medium', 'Long')
        style: Writing style (e.g. 'Conversational', 'Technical', 'Storytelling')
        additional_instructions: Optional user-provided constraints

    Returns:
        A structured, fully assembled prompt string ready for LLM inference.
    """
    # 1. Resolve role persona
    role_description = ROLE_DEFINITIONS.get(content_type, "an expert content strategist and professional writer")

    # 2. Resolve content-specific requirements
    content_rules = CONTENT_TYPE_RULES.get(content_type, CUSTOM_REQUIREMENTS)

    # 3. Resolve length guidelines
    length_category = length if length in LENGTH_GUIDELINES else "Medium"
    length_mapping = LENGTH_GUIDELINES.get(length_category, LENGTH_GUIDELINES["Medium"])
    length_rule = length_mapping.get(content_type, length_mapping["default"])

    # 4. Handle additional instructions formatting
    extra_instructions_section = ""
    if additional_instructions and additional_instructions.strip():
        extra_instructions_section = f"""
Additional User Instructions:
{additional_instructions.strip()}
""".strip()
    else:
        extra_instructions_section = "Additional User Instructions:\nNone provided. Follow best industry standards for this content type."

    # 5. Assemble modular prompt
    prompt = f"""
You are {role_description}.

Your task is to generate exceptional, high-converting, and audience-tailored {content_type} based strictly on the parameters below.

============================================================
CONTENT SPECIFICATIONS
============================================================
- Content Type: {content_type}
- Primary Topic / Context:
{topic.strip()}

- Target Audience: {audience or 'General Audience'}
- Tone of Voice: {tone or 'Professional'}
- Writing Style: {style or 'Conversational'}
- Target Length: {length or 'Medium'} ({length_rule})

============================================================
CONTENT-SPECIFIC FORMATTING REQUIREMENTS
============================================================
{content_rules}

============================================================
USER-SPECIFIED CONSTRAINTS
============================================================
{extra_instructions_section}

============================================================
OUTPUT QUALITY AND HYGIENE RULES
============================================================
1. Stay laser-focused on the topic and target audience.
2. Directly output the final content in clean, beautifully formatted Markdown (headings, bullet points, bolding).
3. Do NOT include conversational filler before or after the content (e.g., do NOT write "Sure, here is your content...", "Hope this helps!", or "As requested...").
4. Do NOT mention that this was generated by an AI, Gemini, or a language model.
5. Ensure grammar, flow, and vocabulary are immaculate and match the requested tone and style.

Now, generate the complete final {content_type}.
""".strip()

    return prompt
