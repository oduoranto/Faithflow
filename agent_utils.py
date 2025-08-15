import os
import logging
import json
from typing import List
from dotenv import load_dotenv
from groq import Groq
import requests

# --------------------------
# Load environment variables
# --------------------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("❌ Missing GROQ_API_KEY in environment variables.")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    raise EnvironmentError("❌ Missing YOUTUBE_API_KEY in environment variables.")

# --------------------------
# Logging configuration
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --------------------------
# Initialize Groq Client
# --------------------------
try:
    groq_client = Groq(api_key=GROQ_API_KEY)
    logger.info("✅ Groq client initialized successfully.")
except Exception as e:
    logger.exception("Failed to initialize Groq client.")
    raise RuntimeError(f"Error initializing Groq client: {e}")

# --------------------------
# LLM Chat Completion
# --------------------------
def chat_with_llm(prompt: str) -> str:
    try:
        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        # Updated for new Groq message object
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.exception("Groq ChatCompletion request failed.")
        raise RuntimeError(f"Groq ChatCompletion failed: {e}")

# --------------------------
# Build prompt for YouTube search
# --------------------------
def build_prompt(topic: str) -> str:
    return (
        f"Recommend 6 recent Christian YouTube videos for mature believers "
        f"focused on the '{topic}' topic. Return JSON array of objects with "
        f"'title', 'url', 'description'. Ensure videos are real, recent, and relevant."
    )

# --------------------------
# YouTube search helper
# --------------------------
def search_youtube_videos(query: str, max_results: int = 6) -> List[dict]:
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        videos = []
        for item in data.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "description": item["snippet"]["description"][:120] + "...",
            })
        return videos
    except Exception as e:
        logger.exception("YouTube search failed.")
        return []

# --------------------------
# Get recommendations
# --------------------------
def get_recommendations(topic: str) -> List[dict]:
    prompt = build_prompt(topic)
    try:
        llm_response = chat_with_llm(prompt)
        videos = json.loads(llm_response)
        return videos
    except Exception:
        logger.warning("LLM failed to return valid JSON, falling back to YouTube search")
        return search_youtube_videos(topic)
