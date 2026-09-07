"""
Flask Backend Application for AI Content Studio.

Exposes web routes for the UI and the /generate API endpoint.
Coordinates request validation, dynamic prompt engineering, and Gemini API inference.
"""

import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from services.prompt_templates import (
    build_prompt,
    get_supported_content_types,
)
from services.gemini_service import (
    generate_content_with_gemini,
    is_api_key_configured,
    get_configured_model,
)

# Load environment variables
load_dotenv()

# Initialize Flask
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ai-content-studio-secret-key")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def index():
    """Render the single-page application interface."""
    return render_template(
        "index.html",
        content_types=get_supported_content_types(),
        model_name=get_configured_model(),
        api_key_configured=is_api_key_configured(),
    )


@app.route("/api/status", methods=["GET"])
def api_status():
    """Health and configuration check endpoint (does NOT expose key)."""
    return jsonify({
        "status": "online",
        "model": get_configured_model(),
        "api_key_configured": is_api_key_configured(),
    })


@app.route("/generate", methods=["POST"])
def generate():
    """
    Handle content generation requests from the frontend.

    Expected JSON body:
    {
        "content_type": str,
        "topic": str,
        "audience": str (optional),
        "tone": str (optional),
        "length": str (optional),
        "style": str (optional),
        "additional_instructions": str (optional)
    }
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request: Expected JSON payload."
            }), 400

        # Extract parameters
        content_type = data.get("content_type", "").strip()
        topic = data.get("topic", "").strip()
        audience = data.get("audience", "General Audience").strip()
        tone = data.get("tone", "Professional").strip()
        length = data.get("length", "Medium").strip()
        style = data.get("style", "Conversational").strip()
        additional_instructions = data.get("additional_instructions", "").strip()

        # Input Validation
        if not topic:
            return jsonify({
                "success": False,
                "error": "Please enter a topic or describe what you want to create."
            }), 400

        supported_types = get_supported_content_types()
        if content_type not in supported_types:
            # Fallback to Custom Content if unspecified
            content_type = "Custom Content"

        # 1. Build prompt via modular prompt engineering
        assembled_prompt = build_prompt(
            content_type=content_type,
            topic=topic,
            audience=audience,
            tone=tone,
            length=length,
            style=style,
            additional_instructions=additional_instructions
        )

        logger.info(f"Generated prompt for '{content_type}' (Topic: {topic[:30]}...)")

        # 2. Call Gemini API service
        result = generate_content_with_gemini(assembled_prompt)

        if not result.get("success"):
            return jsonify({
                "success": False,
                "error": result.get("error", "Unable to generate content right now. Please check your API configuration.")
            }), 500

        return jsonify({
            "success": True,
            "content": result["content"],
            "model": result.get("model", get_configured_model()),
            "content_type": content_type
        })

    except Exception as e:
        logger.error(f"Unexpected error in /generate endpoint: {str(e)}")
        return jsonify({
            "success": False,
            "error": "An unexpected server error occurred. Please try again."
        }), 500


@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return jsonify({"success": False, "error": "Endpoint not found."}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"success": False, "error": "Internal server error."}), 500


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5050))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print("\n=======================================================")
    print(f"[*] AI Content Studio is starting on http://127.0.0.1:{port}")
    print(f"[*] Gemini API Configured: {is_api_key_configured()}")
    print(f"[*] Active Model: {get_configured_model()}")
    print("=======================================================\n")
    app.run(host="127.0.0.1", port=port, debug=debug)
