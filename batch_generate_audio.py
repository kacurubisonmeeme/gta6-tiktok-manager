"""
Batch Audio Generator for GTA 6 TikTok Pilots.
Generates voiceovers for all posts in the queue.
Run: python batch_generate_audio.py
"""
import sys
import os
import json
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from core.audio_engine import AudioEngine
from config import POSTS_QUEUE_FILE

def main():
    print("=" * 65)
    print("🎙️ GTA 6 TIKTOK - BATCH VOICEOVER GENERATOR")
    print("=" * 65)

    if not POSTS_QUEUE_FILE.exists():
        print("❌ No posts queue found at:", POSTS_QUEUE_FILE)
        return

    with open(POSTS_QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if not queue:
        print("❌ Queue is empty.")
        return

    audio_engine = AudioEngine()
    print(f"Found {len(queue)} posts in queue. Generating voiceovers...\n")

    for idx, post in enumerate(queue, 1):
        pid = post.get("id", f"post_{idx}")
        title = post.get("title", f"Pilot {idx}")
        narration = post.get("narration", "")

        if not narration:
            print(f"[{idx}/{len(queue)}] ⚠️ Skipping {pid} (No narration text)")
            continue

        filename_base = f"{pid.lower()}_voiceover"
        print(f"[{idx}/{len(queue)}] 🎙️ Generating audio for {pid} (\"{title[:35]}...\")...")
        
        result = audio_engine.generate_narration(narration, filename_base=filename_base)
        
        if result.get("success"):
            post["audio_file"] = result.get("file_path")
            post["audio_filename"] = result.get("filename")
            post["audio_engine"] = result.get("engine")
            print(f"       ✅ Saved: {result.get('filename')} (via {result.get('engine')})")
        else:
            print(f"       ❌ Failed: {result.get('error')}")

    # Save updated queue with audio paths
    with open(POSTS_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)

    print("\n" + "=" * 65)
    print("🎉 ALL VOICEOVER AUDIO FILES GENERATED!")
    print(f"📂 Location: {audio_engine.output_dir}")
    print("=" * 65)

if __name__ == "__main__":
    main()
