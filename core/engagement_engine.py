"""
Engagement Engine for GTA 6 TikTok Page.
Specializes in comment section growth hacks, conversational replies, pinned comments,
and converting top comments into follow-up video scripts.
"""
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from core.ai_client import AIContentEngine
from core.templates import PINNED_COMMENT_FORMULAS
from config import ENGAGEMENT_LOG_FILE

class EngagementEngine:
    def __init__(self, ai_client: Optional[AIContentEngine] = None):
        self.ai = ai_client or AIContentEngine()
        self.log_file = ENGAGEMENT_LOG_FILE

    def get_comment_replies(self, comment_text: str) -> Dict[str, str]:
        """Generates 3 tactical reply variations to boost thread length and video reach."""
        replies = self.ai.generate_comment_replies(comment_text)
        self._log_interaction(comment_text, replies)
        return replies

    def generate_pinned_comment(self, post_topic: str = "") -> str:
        """Returns a high-conversion pinned comment designed to spark 50+ replies."""
        import random
        base = random.choice(PINNED_COMMENT_FORMULAS)
        if post_topic:
            return f"🚨 QUESTION: Regarding {post_topic}... what's your prediction? Best theory gets pinned! 👇"
        return base

    def comment_to_video_reply_concept(self, username: str, comment_text: str) -> Dict[str, Any]:
        """Converts a top viewer comment into a full 'Replying to @username' TikTok script."""
        topic = f"Reply to {username}: {comment_text}"
        script = self.ai.generate_video_package(
            topic=topic,
            pillar="Community Debates & Comment Video Replies",
            tone="debate_provoker"
        )
        script["hook"] = f"Replying to @{username.replace('@', '')} — this is the one question everyone has about GTA 6..."
        script["title"] = f"Video Reply to @{username}: {comment_text[:40]}..."
        return script

    def _log_interaction(self, comment: str, replies: Dict[str, str]):
        """Persists engagement interactions for tracking."""
        try:
            records = []
            if self.log_file.exists():
                with open(self.log_file, "r", encoding="utf-8") as f:
                    records = json.load(f)
            records.append({
                "timestamp": datetime.now().isoformat(),
                "comment": comment,
                "replies": replies
            })
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(records[-200:], f, indent=2)  # Keep last 200
        except Exception:
            pass
