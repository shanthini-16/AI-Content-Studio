"""
Google Gemini Service Module for AI Content Studio.

Handles secure communication with the Google Gemini API using the official
google-genai SDK. Keeps all API credentials and connection handling encapsulated.
"""

import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ensure environment variables are loaded
load_dotenv()

# Default Gemini model
DEFAULT_MODEL = "gemini-3.5-flash-lite"


def get_api_key() -> str:
    """Retrieve the Gemini API key from environment variables."""
    load_dotenv(override=True)
    return os.getenv("GEMINI_API_KEY", "").strip()


def get_configured_model() -> str:
    """Retrieve the configured model name or fallback to default."""
    return os.getenv("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def is_api_key_configured() -> bool:
    """Check if a valid non-placeholder API key is set."""
    key = get_api_key()
    if not key:
        return False
    if "your_api_key" in key.lower() or "your_gemini_api_key" in key.lower():
        return False
    return True


def generate_content_with_gemini(prompt: str) -> Dict[str, Any]:
    """
    Send prompt to Google Gemini and return the generated content.

    Parameters:
        prompt: The assembled prompt string from prompt_templates.py

    Returns:
        Dict with "success" (bool), "content" (str if success), or "error" (str if failed).
    """
    # 1. Validate API Key availability
    if not is_api_key_configured():
        logger.warning("Attempted generation without valid GEMINI_API_KEY.")
        return {
            "success": False,
            "error": "Gemini API key is missing or not configured. Please open the .env file in the project folder, set your GEMINI_API_KEY from Google AI Studio, and restart the server."
        }

    api_key = get_api_key()
    model_name = get_configured_model()

    # 2. Call Gemini API
    try:
        client = genai.Client(api_key=api_key)
        logger.info(f"Dispatching generation request to model: {model_name}")

        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        # 3. Extract text content
        if not response or not response.text:
            return {
                "success": False,
                "error": "Gemini returned an empty response. Please try adjusting your prompt parameters."
            }

        return {
            "success": True,
            "content": response.text.strip(),
            "model": model_name
        }

    except errors.ClientError as ce:
        error_str = str(ce)
        logger.error(f"Gemini ClientError: {error_str}")
        if "API_KEY_INVALID" in error_str or "400" in error_str or "PERMISSION_DENIED" in error_str:
            return {
                "success": False,
                "error": "Invalid or unauthorized Gemini API key. Please verify your GEMINI_API_KEY in the .env file."
            }
        elif "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
            return {
                "success": False,
                "error": "Gemini API quota exceeded or rate limit reached. Please wait a minute before retrying."
            }
        else:
            return {
                "success": False,
                "error": "Gemini API rejected the request. Please verify your input parameters and API key permissions."
            }

    except errors.ServerError as se:
        logger.error(f"Gemini ServerError: {se}")
        return {
            "success": False,
            "error": "Google Gemini service is temporarily experiencing high traffic. Please try again shortly."
        }

    except Exception as e:
        error_msg = str(e)
        # Prevent any accidental leakage of the API key string
        if api_key and api_key in error_msg:
            error_msg = error_msg.replace(api_key, "[REDACTED_API_KEY]")

        logger.error(f"Unexpected generation error: {error_msg}")
        return {
            "success": False,
            "error": f"Failed to generate content: {error_msg}"
        }
