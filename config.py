"""
Configuration settings for GTA 6 TikTok Page Manager.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Ensure data directory exists
DATA_DIR.mkdir(parents=True, exist_ok=True)

POSTS_QUEUE_FILE = DATA_DIR / "posts_queue.json"
ENGAGEMENT_LOG_FILE = DATA_DIR / "engagement_log.json"
GTA6_KNOWLEDGE_FILE = DATA_DIR / "gta6_knowledge.json"

# Gemini API Key (optional - system works offline with smart templates or online with Gemini)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# TikTok Best Posting Times for Gaming / GTA Niche (Local time)
PEAK_POSTING_HOURS = [
    {"slot": "Morning Hype", "time": "11:30 AM", "niche": "News, quick leaks & morning updates"},
    {"slot": "Afternoon Rush", "time": "03:30 PM", "niche": "Trailer breakdowns & comparison clips"},
    {"slot": "Prime Time Peak", "time": "07:00 PM", "niche": "Deep theories, debates & character lore"},
    {"slot": "Late Night Viral", "time": "09:30 PM", "niche": "Memes, Florida Man references & polls"}
]

# Supported Content Pillars
CONTENT_PILLARS = [
    "Trailer & Teaser Breakdowns",
    "Hidden Easter Eggs & Map Details",
    "Lucia & Jason Dynamics & Theories",
    "Rockstar Technology, AI & Leaks",
    "Real Florida vs. Leonida Comparisons",
    "Release Date Rumors & Take-Two Updates",
    "Community Debates & Comment Video Replies"
]

# Account Tone Profiles
ACCOUNT_TONES = {
    "hype": "Excited, fast-paced, high energy, viral gamer tone",
    "lore_expert": "Deeply knowledgeable, analytical, noticing details everyone missed",
    "satirical": "Florida-man humor, witty, mocking ridiculous gaming rumors",
    "debate_provoker": "Controversial takes designed to make hundreds of people comment"
}
