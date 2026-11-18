"""
AI Client integrating Gemini API for dynamic script generation and comment replies,
with a robust fallback to offline algorithmic generators if no API key is provided.
"""
import os
import json
import random
from typing import Dict, Any, List, Optional
from core.templates import (
    VIRAL_HOOKS, CTA_TEMPLATES, PINNED_COMMENT_FORMULAS,
    COMMENT_REPLY_ARCHETYPES, OFFLINE_SCRIPT_TEMPLATES
)

class AIContentEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.client = None
        self._init_client()

    def _init_client(self):
        if not self.api_key:
            return
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except Exception:
            self.client = None

    def generate_video_package(self, topic: str, pillar: str, tone: str = "hype") -> Dict[str, Any]:
        """Generates a complete TikTok video package: Hook, Script, Visual cues, Audio, Caption, CTA, Pinned Comment."""
        if self.client:
            try:
                return self._generate_with_gemini(topic, pillar, tone)
            except Exception:
                # Fallback to local intelligent generator
                pass
        return self._generate_offline(topic, pillar, tone)

    def _generate_with_gemini(self, topic: str, pillar: str, tone: str) -> Dict[str, Any]:
        prompt = f"""
You are the world's #1 TikTok content strategist & scriptwriter specialized in Grand Theft Auto 6 (GTA 6).
Create a high-retention, viral short-form TikTok video script (20-35 seconds long) on this topic:
Topic: "{topic}"
Pillar: "{pillar}"
Tone: "{tone}"

Output valid JSON ONLY with the following exact keys:
{{
  "title": "Short catchy title",
  "pillar": "{pillar}",
  "hook": "0-3 second explosive attention grabber",
  "visual_cues": [
    "[0-3s] specific visual description / b-roll to show",
    "[3-10s] visual description",
    "[10-20s] visual description",
    "[20-30s] visual description"
  ],
  "narration": "Full spoken voiceover script, punchy, engaging, 60-80 words",
  "cta": "Engaging call to action asking a specific debate question for comments",
  "caption": "TikTok caption under 150 characters with 4-6 viral hashtags",
  "sound_recommendation": "Suggested audio vibe / trending sound",
  "pinned_comment": "First comment the creator will pin to drive 100+ replies"
}}
"""
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )
        return json.loads(response.text)

    def _generate_offline(self, topic: str, pillar: str, tone: str) -> Dict[str, Any]:
        """Smart offline template & heuristic generator for GTA 6 content."""
        # Find matching template or generate dynamic hybrid
        matching = [t for t in OFFLINE_SCRIPT_TEMPLATES if pillar.lower() in t["pillar"].lower()]
        base = random.choice(matching) if matching else random.choice(OFFLINE_SCRIPT_TEMPLATES)
        
        hook = random.choice(VIRAL_HOOKS)
        cta = random.choice(CTA_TEMPLATES)
        pinned = random.choice(PINNED_COMMENT_FORMULAS)
        
        if topic and topic.strip():
            title = f"GTA 6 Breakdown: {topic.strip()}"
            narration = f"You won't believe what Rockstar just showed regarding {topic.strip()}. {base['narration']}"
        else:
            title = base["title"]
            narration = base["narration"]

        return {
            "title": title,
            "pillar": pillar,
            "hook": hook if not topic else f"Stop scrolling if you care about {topic} in GTA 6...",
            "visual_cues": base["visual_cues"],
            "narration": narration,
            "cta": cta,
            "caption": f"Is Rockstar really cooking with this? 🤯 {cta.split('?')[0]}? #GTA6 #GTAVI #RockstarGames #GamingOnTikTok #ViceCity",
            "sound_recommendation": base["sound_recommendation"],
            "pinned_comment": pinned
        }

    def generate_comment_replies(self, comment_text: str, tone: str = "engagement") -> Dict[str, str]:
        """Generates 3 variations of replies to a TikTok comment:
           1. Engagement Magnet (provokes another reply)
           2. Witty / Banter (viral humor)
           3. Lore Expert (factual Rockstar detail)
        """
        if self.client:
            try:
                prompt = f"""
You are the community manager for a huge GTA 6 TikTok channel.
A viewer just left this comment on a video:
"{comment_text}"

Generate 3 different reply styles to maximize engagement and get more comments:
1. "engagement_magnet": Asks an intriguing counter-question so they HAVE to reply back.
2. "witty_banter": Humorous, witty, friendly Florida/gamer banter.
3. "lore_expert": Analytical answer referencing Rockstar details, trailers, or patents.

Output strictly valid JSON with keys: "engagement_magnet", "witty_banter", "lore_expert".
"""
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
                    config={"response_mime_type": "application/json"}
                )
                return json.loads(response.text)
            except Exception:
                pass

        # Offline fallback categorized reply selection
        comment_lower = comment_text.lower()
        if any(w in comment_lower for w in ["delay", "2026", "cancel", "never", "take long"]):
            cat = "hater_delay"
        elif any(w in comment_lower for w in ["fps", "ps5", "xbox", "pc", "console", "frame", "60"]):
            cat = "fps_console"
        elif any(w in comment_lower for w in ["story", "lucia", "jason", "ending", "die", "betray"]):
            cat = "story_theory"
        elif any(w in comment_lower for w in ["florida", "alligator", "miami", "real", "joker"]):
            cat = "florida_man"
        else:
            cat = "generic_engagement"

        replies = COMMENT_REPLY_ARCHETYPES[cat]
        return {
            "engagement_magnet": replies[0],
            "witty_banter": replies[1] if len(replies) > 1 else replies[0],
            "lore_expert": replies[2] if len(replies) > 2 else replies[0]
        }
