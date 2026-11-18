"""
Schedule & Post Queue Manager for GTA 6 TikTok Page.
Handles post queues, optimal TikTok publishing time slots, and status progression.
"""
import json
import uuid
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from config import POSTS_QUEUE_FILE, PEAK_POSTING_HOURS

class ScheduleManager:
    def __init__(self):
        self.file_path = POSTS_QUEUE_FILE
        self._ensure_file()

    def _ensure_file(self):
        if not self.file_path.exists():
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def load_queue(self) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_queue(self, queue: List[Dict[str, Any]]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(queue, f, indent=2)

    def add_to_queue(self, video_data: Dict[str, Any], scheduled_date: Optional[str] = None, slot_name: str = "Prime Time Peak") -> Dict[str, Any]:
        """Adds a video script to the posting schedule queue."""
        queue = self.load_queue()
        
        # Calculate scheduled time
        target_slot = next((s for s in PEAK_POSTING_HOURS if s["slot"].lower() == slot_name.lower()), PEAK_POSTING_HOURS[2])
        if not scheduled_date:
            scheduled_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        item = {
            "id": str(uuid.uuid4())[:8],
            "title": video_data.get("title", "Untitled GTA 6 Video"),
            "pillar": video_data.get("pillar", "General"),
            "hook": video_data.get("hook", ""),
            "narration": video_data.get("narration", ""),
            "visual_cues": video_data.get("visual_cues", []),
            "cta": video_data.get("cta", ""),
            "caption": video_data.get("caption", ""),
            "sound_recommendation": video_data.get("sound_recommendation", ""),
            "pinned_comment": video_data.get("pinned_comment", ""),
            "scheduled_date": scheduled_date,
            "scheduled_time": target_slot["time"],
            "slot_name": target_slot["slot"],
            "status": "SCRIPTED",  # SCRIPTED, RECORDED, POSTED
            "created_at": datetime.now().isoformat(),
            "performance": {
                "views": 0,
                "likes": 0,
                "comments": 0,
                "shares": 0
            }
        }
        queue.append(item)
        self.save_queue(queue)
        return item

    def update_status(self, post_id: str, new_status: str) -> bool:
        """Updates status to SCRIPTED, RECORDED, or POSTED."""
        queue = self.load_queue()
        for p in queue:
            if p["id"] == post_id:
                p["status"] = new_status
                self.save_queue(queue)
                return True
        return False

    def update_metrics(self, post_id: str, views: int, likes: int, comments: int, shares: int = 0) -> bool:
        """Logs performance metrics for a posted video."""
        queue = self.load_queue()
        for p in queue:
            if p["id"] == post_id:
                p["performance"] = {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "shares": shares
                }
                self.save_queue(queue)
                return True
        return False

    def get_upcoming(self) -> List[Dict[str, Any]]:
        queue = self.load_queue()
        return [p for p in queue if p.get("status") in ("SCRIPTED", "RECORDED")]

    def get_posted(self) -> List[Dict[str, Any]]:
        queue = self.load_queue()
        return [p for p in queue if p.get("status") == "POSTED"]

    def delete_post(self, post_id: str) -> bool:
        queue = self.load_queue()
        initial_len = len(queue)
        queue = [p for p in queue if p["id"] != post_id]
        if len(queue) < initial_len:
            self.save_queue(queue)
            return True
        return False
