# AI Content Studio ✍️🚀
> **"Generate smarter content with AI."**

A complete, full-stack Generative AI web application built as an **internship mini-project**. **AI Content Studio** empowers users to generate diverse, high-quality, audience-tailored digital content using **Google Gemini** and modern **Prompt Engineering** techniques.

---

## 📑 Table of Contents
1. [Project Overview](#-project-overview)
2. [Key Features](#-key-features)
3. [Technologies Used](#-technologies-used)
4. [Generative AI Concepts Demonstrated](#-generative-ai-concepts-demonstrated)
5. [System Architecture](#-system-architecture)
6. [Project Structure](#-project-structure)
7. [Installation & Setup (Windows)](#-installation--setup-windows)
8. [Running the Application](#-running-the-application)
9. [Interview Q&A Guide](#-interview-qa-guide)
10. [Future Enhancements](#-future-enhancements)

---

## 🌟 Project Overview

Creating digital content across different channels (blogs, social media, marketing emails, sales copy) requires different formats, tones, lengths, and structures. A simple, raw question sent to an LLM usually produces generic or improperly formatted responses.

**AI Content Studio** solves this through **modular prompt engineering**. Instead of sending raw user input directly to the model, the application dynamically constructs an expert prompt combining:
- **Role Persona**: Tailored expertise for the chosen medium (e.g., SEO specialist for blogs, growth hacker for LinkedIn).
- **Task & Domain Requirements**: Format-specific structures (hooks, subheadings, CTAs, hashtags, timestamps).
- **Context Injection**: User topic and additional instructions.
- **Parametric Constraints**: Target audience, tone of voice, writing style, and length bounds.

The result is consistent, high-utility, ready-to-publish content.

---

## ⚡ Key Features

### 1. 9 Supported Content Formats
- **Blog Post**: SEO-optimized title, introduction hook, Markdown subheadings (H2/H3), concrete examples, and conclusion.
- **LinkedIn Post**: Scroll-stopping opening hook, short punchy paragraphs, actionable insights, engagement question, and relevant hashtags.
- **Social Media Caption**: Snappy opener, conversational tone, tasteful emojis, engagement callout, and hashtag cluster.
- **Email**: Multiple high-converting subject line variations, professional greeting, body copy, unambiguous CTA, and formal sign-off.
- **Product Description**: Catchy product title, customer pain point identification, Feature-to-Benefit breakdowns, and conversion CTA.
- **Advertisement Copy**: Multiple headline formulas (Value, Problem, Curiosity), unique value proposition (UVP), social proof cues, and direct CTA.
- **YouTube Description**: Search-optimized title suggestions, comprehensive video summary, chapter timestamp placeholders, and keyword tags.
- **Creative Story**: Immersive world-building, character introductions, rising conflict, dynamic pacing, and satisfying climax.
- **Custom Content**: General-purpose high-polish generation adhering strictly to custom parameters.

### 2. Fine-Grained Customization
- **Topic / Context**: Large input area with character count and **one-click example tags** (*AI in Education*, *Future of Generative AI*, *Benefits of Python*, *Sustainable Technology*, *Remote Work Trends*).
- **Target Audience**: *General Audience*, *Students*, *Developers*, *Professionals*, *Customers*, *Business Owners*, or *Custom...*.
- **Tone**: *Professional*, *Friendly*, *Casual*, *Persuasive*, *Informative*, *Creative*, *Formal*.
- **Length**: *Short* (concise/punchy), *Medium* (balanced depth), *Long* (in-depth comprehensive coverage).
- **Writing Style**: *Simple*, *Conversational*, *Professional*, *Storytelling*, *Technical*, *SEO-friendly*.
- **Additional Instructions**: Custom user guidelines (e.g., "Include a case study and end with a question").

### 3. Output Management Toolbar
- **Live Markdown Preview**: Formatted headings, bullet lists, blockquotes, and code snippets powered by Marked.js.
- **Metrics Bar**: Live word count, character count, and content type badge.
- **One-Click Copy**: Copies generated text to clipboard with animated visual feedback.
- **Regenerate**: Immediately re-triggers generation with the same settings for fresh variations.
- **Download**: Exports output as a clean `.txt` file (`<content_type>_<timestamp>.txt`).
- **Clear**: Resets generated preview and stats.

### 4. Robust UX & Error Handling
- Smooth loading animation with `"Creating your content..."` state.
- Graceful API key validation with actionable user instructions.
- Protection against empty submissions and network timeouts.

---

## 🛠 Technologies Used

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python 3.10+ | Core application runtime |
| **Framework** | Flask | Lightweight WSGI web server and REST API routing |
| **LLM Provider** | Google Gemini API (`google-genai` SDK) | State-of-the-art GenAI text generation |
| **Model** | `gemini-3.5-flash-lite` | Fast, high-quality, cost-efficient Google Gemini multimodal LLM |
| **Environment** | `python-dotenv` | Secure configuration management |
| **Frontend** | HTML5 / CSS3 / Vanilla JavaScript | Responsive single-page application |
| **Markdown Parser** | Marked.js (CDN) | Client-side rendering of structured Markdown responses |

---

## 🧠 Generative AI Concepts Demonstrated

This project is specifically designed to showcase core Generative AI and LLM engineering fundamentals:

1. **Prompt Engineering Architecture**:
   Prompt construction is isolated into a dedicated service layer (`services/prompt_templates.py`), preventing hardcoded queries.
2. **Role / Persona Prompting**:
   Assigning the model an authoritative role (e.g., *"You are an influential executive thought leader and professional brand strategist"*) conditions the model's latent weights to output higher-caliber vocabulary and formatting.
3. **Context Injection & Parameterization**:
   Dynamically inserting user-provided parameters (`topic`, `audience`, `tone`, `style`, `length`) into structural prompt slots.
4. **Task-Specific Output Guardrails**:
   Enforcing strict output rules (e.g., forbidding conversational AI fluff like *"Sure, here is your article"*, preventing mention of AI generation, and enforcing Markdown formatting).
5. **Separation of Concerns**:
   Decoupling the API provider (`gemini_service.py`), prompt logic (`prompt_templates.py`), and transport layer (`app.py`).

---

## 🏗 System Architecture

```
┌────────────────────────────────────────────────────────┐
│                   User Browser (UI)                    │
│   • Content Settings Form (Topic, Audience, Tone...)   │
│   • Live Markdown Display & Metric Counters            │
│   • Copy / Download / Regenerate Actions               │
└───────────────────────────┬────────────────────────────┘
                            │
                            │  HTTP POST /generate (JSON Payload)
                            ▼
┌────────────────────────────────────────────────────────┐
│               Flask Backend (`app.py`)                 │
│   • Request Validation (non-empty topic, valid type)   │
│   • Route Dispatching & Error Handling                 │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│      Prompt Builder (`services/prompt_templates.py`)   │
│   • Resolves Role Persona                              │
│   • Injects Formatting Guidelines (BLOG/EMAIL/etc.)    │
│   • Applies Length & Tone Constraints                  │
│   • Generates Assembled Prompt String                  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│       Gemini Service (`services/gemini_service.py`)    │
│   • Validates GEMINI_API_KEY from .env                 │
│   • Initializes `google.genai.Client`                  │
│   • Calls `client.models.generate_content`             │
│   • Catches API errors & sanitizes output              │
└───────────────────────────┬────────────────────────────┘
                            │
                            │  gRPC / HTTPS
                            ▼
┌────────────────────────────────────────────────────────┐
│                   Google Gemini LLM                    │
│               (`gemini-3.5-flash-lite`)                │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```text
AI-Content-Studio/
│
├── app.py                      # Flask server, route definitions, API endpoints
├── requirements.txt            # Minimal, exact project dependencies
├── .env                        # Local environment variables (API keys - gitignored)
├── .env.example                # Example environment configuration template
├── .gitignore                  # Git exclusion rules
├── README.md                   # Project documentation & interview guide
│
├── services/                   # Modular business logic
│   ├── __init__.py             # Package initializer
│   ├── gemini_service.py       # Google Gemini SDK integration & error handling
│   └── prompt_templates.py     # Prompt engineering templates & builder system
│
├── templates/
│   └── index.html              # Responsive single-page web UI
│
└── static/
    ├── css/
    │   └── style.css           # Modern dark UI, cards, layout, animations
    └── js/
        └── script.js           # Fetch API, clipboard copy, file download, metrics
```

---

## 💻 Installation & Setup (Windows)

Follow these exact steps in **PowerShell** or **Command Prompt**:

### 1. Open Terminal and Navigate to Project
```powershell
cd C:\Users\Shanthini\.gemini\antigravity\scratch\AI-Content-Studio
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```
*(You will see `(venv)` appear in your command prompt).*

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Your Gemini API Key
1. Get a free API key from [Google AI Studio](https://aistudio.google.com/).
2. Open `.env` in any text editor (Notepad, VS Code):
```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere
GEMINI_MODEL=gemini-3.5-flash-lite
FLASK_PORT=5050
FLASK_DEBUG=True
```
3. Save the file.

---

## 🚀 Running the Application

### 1. Start the Flask Server
```powershell
python app.py
```

### 2. Access the Web Application
Open your browser and navigate to:
```
http://127.0.0.1:5050
```

### 3. Quick Demonstration Steps
1. Click any example tag (e.g. **"AI in Education"**).
2. Choose a Content Type (e.g. **LinkedIn Post** or **Blog Post**).
3. Select an Audience (e.g. **Students**), Tone (**Engaging/Professional**), and Length (**Medium**).
4. Click **Generate Content**.
5. Observe the live loading indicator, generated Markdown output, and word/char count metrics.
6. Test the **Copy**, **Download**, and **Regenerate** buttons.

---

## 🎤 Interview Q&A Guide

When discussing this project during an internship interview:

**Q1: Why did you separate prompt construction into `prompt_templates.py`?**
> *"In production Generative AI applications, prompt engineering is software engineering. Hardcoding prompt strings inside route handlers leads to brittle, untestable code. By isolating prompt templates into a dedicated service, we can test prompt logic independently, version-control templates, and adjust instructions without touching Flask routes."*

**Q2: How does the application prevent LLM hallucinations or off-topic outputs?**
> *"We use role prompting, explicit task boundaries, format-specific structural rules (like H2 headings for blogs or subject lines for emails), and negative constraints (such as 'Do not include conversational filler' and 'Do not mention you are an AI')."*

**Q3: How do you handle security for the API key?**
> *"The API key is never exposed to the client-side JavaScript. It is stored in `.env`, loaded into memory via `python-dotenv`, and accessed strictly inside the server-side `gemini_service.py`. `.env` is explicitly listed in `.gitignore` to prevent leaking credentials to version control."*

**Q4: Which Gemini model did you use and why?**
> *"We used `gemini-3.5-flash-lite`. It delivers fast 3-second latency, excellent instruction following, and high reasoning fidelity while remaining cost-effective for high-frequency content generation tasks."*

---

## 🔮 Future Enhancements

1. **Server-Sent Events (SSE) / Streaming**: Stream LLM tokens in real-time as they generate.
2. **User Authentication & Saved History**: SQLite / PostgreSQL integration to let users save past drafts.
3. **Multi-Model Comparison**: Side-by-side output comparison between `gemini-2.5-flash` and `gemini-2.5-pro`.
4. **Export to Multiple Formats**: Export directly to PDF or HTML in addition to TXT.
5. **Multilingual Generation**: Add a target language selector for automated localization.

---

**Developed with ❤️ for Generative AI Internship Mini-Project.**
