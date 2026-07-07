"""
BearDiary AI - Groq AI Helper 🤖💌
Mood analysis + comfort letter generation
"""

import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

# Load environment variables safely
load_dotenv()

# Initialize Groq client
_client = None

def get_client():
    """Lazy-load Groq client (only when needed)"""
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found! Check your .env file 🔐")
        _client = Groq(api_key=api_key)
    return _client


# ============================================
# 💌 THE COZY AI PROMPT
# ============================================
SYSTEM_PROMPT = """You are BearBestie 🐻 — the warmest, gentlest AI journaling companion. 
You read someone's journal entry and respond with genuine care, like a best friend who happens to be a soft teddy bear.

Your personality:
- Warm, gentle, non-judgmental
- Uses cozy language ("sweet friend", "dear one", "lovely soul")
- Occasionally uses cute emojis (🧸🎀💕🌸✨)
- NEVER dismissive or preachy
- Celebrates joys, sits with sadness, encourages gently

You MUST respond with ONLY valid JSON in this exact format (no markdown, no extra text):

{
  "mood": "one of: happy, sad, anxious, peaceful, excited, tired, angry, grateful, hopeful, confused",
  "mood_emoji": "single relevant emoji",
  "vibe_word": "one cute aesthetic word describing today (e.g. 'cinnamon', 'sunlit', 'stormy', 'cozy', 'blooming')",
  "letter": "A warm 3-4 sentence letter back to the writer. Be specific to what they wrote. Be gentle and cozy.",
  "affirmation": "One short affirmation sentence for them today"
}
"""


def analyze_entry(journal_text: str) -> dict:
    """
    Analyze a journal entry and return mood + comfort letter.
    Returns a dict with: mood, mood_emoji, vibe_word, letter, affirmation
    """
    client = get_client()
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here is today's journal entry:\n\n{journal_text}"}
            ],
            temperature=0.7,
            max_tokens=500,
            response_format={"type": "json_object"}
        )
        
        raw_response = response.choices[0].message.content
        
        # Clean up any potential markdown wrapping
        cleaned = re.sub(r'^```(?:json)?\s*|\s*```$', '', raw_response.strip(), flags=re.MULTILINE)
        
        result = json.loads(cleaned)
        
        # Ensure all keys exist (fallbacks for safety)
        return {
            "mood": result.get("mood", "peaceful"),
            "mood_emoji": result.get("mood_emoji", "💕"),
            "vibe_word": result.get("vibe_word", "cozy"),
            "letter": result.get("letter", "Thank you for sharing with me today 🧸"),
            "affirmation": result.get("affirmation", "You are loved. You are enough. 💕")
        }
        
    except json.JSONDecodeError as e:
        return {
            "mood": "peaceful",
            "mood_emoji": "🧸",
            "vibe_word": "cozy",
            "letter": f"I read your entry with care, sweet friend 🎀 Something went wonky with my response, but your feelings are valid and heard. 💕",
            "affirmation": "You showed up today. That matters. ✨"
        }
    except Exception as e:
        raise Exception(f"AI analysis failed: {str(e)}")