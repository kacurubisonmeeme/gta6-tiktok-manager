"""
Content Engine for GTA 6 TikTok Page.
Handles video packaging, viral hooks, script structuring, and hashtag optimization.
"""
from typing import Dict, Any, List, Optional
import random
from core.ai_client import AIContentEngine
from config import CONTENT_PILLARS, ACCOUNT_TONES

class ContentEngine:
    def __init__(self, ai_client: Optional[AIContentEngine] = None):
        self.ai = ai_client or AIContentEngine()

    def create_video_script(self, topic: str = "", pillar: str = "", tone: str = "hype") -> Dict[str, Any]:
        """Creates a complete TikTok production blueprint for a video."""
        if not pillar or pillar not in CONTENT_PILLARS:
            pillar = random.choice(CONTENT_PILLARS)
        if tone not in ACCOUNT_TONES:
            tone = "hype"

        package = self.ai.generate_video_package(topic=topic, pillar=pillar, tone=tone)
        return package

    def suggest_topics(self) -> List[Dict[str, str]]:
        """Returns trending content prompts ready to produce."""
        return [
            {
                "title": "Trailer 2 Release Date Clues",
                "pillar": "Release Date Rumors & Take-Two Updates",
                "hook": "Rockstar just dropped a massive hint about Trailer 2 in their latest post."
            },
            {
                "title": "The Leonida Prison Escape Mechanic",
                "pillar": "Lucia & Jason Dynamics & Theories",
                "hook": "Notice how Lucia starts with an ankle monitor? Here's what that actually means for gameplay."
            },
            {
                "title": "Will GTA 6 Have Dynamic NPC Memory?",
                "pillar": "Rockstar Technology, AI & Leaks",
                "hook": "If you fight an NPC in GTA 6, they might actually hunt you down later."
            },
            {
                "title": "Vice City Map vs. Real Miami",
                "pillar": "Real Florida vs. Leonida Comparisons",
                "hook": "We mapped the real Miami streets against GTA 6 and the scale is mind-blowing."
            },
            {
                "title": "Hidden Underwater Secrets in the Keys",
                "pillar": "Hidden Easter Eggs & Map Details",
                "hook": "The underwater map in GTA 6 is secretly bigger than the entire landmass."
            }
        ]
