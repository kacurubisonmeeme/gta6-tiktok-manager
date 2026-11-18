"""
GTA 6 TikTok Page Manager - Main Command Line Interface.
Run: python manager.py
"""
import sys
import os
import json
from datetime import datetime

# Add local path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONTENT_PILLARS, PEAK_POSTING_HOURS, ACCOUNT_TONES
from core.content_engine import ContentEngine
from core.engagement_engine import EngagementEngine
from core.schedule_manager import ScheduleManager

def print_banner():
    banner = r"""
 =========================================================================
   🌴 GTA 6 TIKTOK PAGE MANAGER & ENGAGEMENT ENGINE 🌴
   Vice City Content Automation, Viral Scripts & Community Growth
 =========================================================================
"""
    print(banner)

def display_menu():
    print("\n[MAIN MENU]")
    print("  1. 🎬 Generate Viral Video Script (Hook, B-Roll, Voiceover, CTA)")
    print("  2. 💬 Comment Reply Assistant (Boost algorithm with 3 reply styles)")
    print("  3. 🎥 Convert Top Comment -> 'Video Reply' Script (Part 2 format)")
    print("  4. 📌 Generate Pinned Comment (Drive instant debate)")
    print("  5. 📅 View Scheduled Post Queue & Update Status")
    print("  6. ⏰ View Optimal TikTok Posting Times for Gaming")
    print("  7. 🌐 Launch Interactive Web Dashboard")
    print("  0. ❌ Exit")
    print("-" * 65)

def format_video_package(pkg: dict):
    print("\n" + "=" * 65)
    print(f"🎬 TITLE: {pkg.get('title')}")
    print(f"🏛️  PILLAR: {pkg.get('pillar')}")
    print("-" * 65)
    print(f"⚡ HOOK (0-3s):")
    print(f"   \"{pkg.get('hook')}\"")
    print("\n🎥 VISUAL / B-ROLL CUES:")
    for cue in pkg.get("visual_cues", []):
        print(f"   • {cue}")
    print("\n🎙️ VOICEOVER NARRATION:")
    print(f"   \"{pkg.get('narration')}\"")
    print(f"\n📢 CALL TO ACTION (CTA):")
    print(f"   \"{pkg.get('cta')}\"")
    print(f"\n🎵 SOUND RECOMMENDATION: {pkg.get('sound_recommendation')}")
    print(f"\n📝 TIKTOK CAPTION:")
    print(f"   {pkg.get('caption')}")
    print(f"\n📌 PINNED COMMENT (Paste right after upload):")
    print(f"   {pkg.get('pinned_comment')}")
    print("=" * 65 + "\n")

def handle_generate_script(content_engine: ContentEngine, schedule_mgr: ScheduleManager):
    print("\n--- 🎬 GENERATE TIKTOK SCRIPT ---")
    print("Select a Content Pillar or press Enter for Random:")
    for idx, p in enumerate(CONTENT_PILLARS, 1):
        print(f"  {idx}. {p}")
    choice = input("\nEnter number (or press Enter): ").strip()
    pillar = ""
    if choice.isdigit() and 1 <= int(choice) <= len(CONTENT_PILLARS):
        pillar = CONTENT_PILLARS[int(choice) - 1]

    topic = input("Enter specific topic/angle (or press Enter for suggested topic): ").strip()
    
    print("\nGenerating viral TikTok blueprint...")
    pkg = content_engine.create_video_script(topic=topic, pillar=pillar)
    format_video_package(pkg)

    save_choice = input("Do you want to add this script to your Posting Schedule Queue? (y/n): ").strip().lower()
    if save_choice == 'y':
        print("\nSelect Posting Time Slot:")
        for idx, s in enumerate(PEAK_POSTING_HOURS, 1):
            print(f"  {idx}. {s['slot']} ({s['time']}) - {s['niche']}")
        slot_choice = input("Choice (1-4, default 3): ").strip()
        slot_name = "Prime Time Peak"
        if slot_choice.isdigit() and 1 <= int(slot_choice) <= len(PEAK_POSTING_HOURS):
            slot_name = PEAK_POSTING_HOURS[int(slot_choice) - 1]["slot"]
        
        date_input = input("Scheduled Date (YYYY-MM-DD, or press Enter for tomorrow): ").strip()
        item = schedule_mgr.add_to_queue(pkg, scheduled_date=date_input if date_input else None, slot_name=slot_name)
        print(f"✅ Added to queue! [Post ID: {item['id']}] Scheduled for {item['scheduled_date']} at {item['scheduled_time']}.")

def handle_comment_reply(engagement_engine: EngagementEngine):
    print("\n--- 💬 TIKTOK COMMENT REPLY ASSISTANT ---")
    comment = input("Paste the viewer's comment: ").strip()
    if not comment:
        print("No comment entered.")
        return

    print("\nAnalyzing comment tone and crafting engagement-boosting replies...")
    replies = engagement_engine.get_comment_replies(comment)
    
    print("\n" + "=" * 60)
    print("🧲 OPTION 1: ENGAGEMENT MAGNET (Forces viewer to reply back):")
    print(f"   \"{replies['engagement_magnet']}\"")
    print("\n😂 OPTION 2: WITTY BANTER (Viral gamer humor / Florida Man tone):")
    print(f"   \"{replies['witty_banter']}\"")
    print("\n🧠 OPTION 3: LORE EXPERT (Analytical, points to Rockstar details):")
    print(f"   \"{replies['lore_expert']}\"")
    print("=" * 60)

def handle_video_reply(engagement_engine: EngagementEngine, schedule_mgr: ScheduleManager):
    print("\n--- 🎥 CONVERT COMMENT TO 'VIDEO REPLY' ---")
    user = input("Viewer's username (e.g. @GamerGuy99): ").strip() or "@viewer"
    comment = input("Viewer's comment to reply to: ").strip()
    if not comment:
        print("Comment required.")
        return

    print(f"\nCrafting 'Replying to {user}' video script...")
    pkg = engagement_engine.comment_to_video_reply_concept(username=user, comment_text=comment)
    format_video_package(pkg)

    save = input("Add this video reply to your queue? (y/n): ").strip().lower()
    if save == 'y':
        item = schedule_mgr.add_to_queue(pkg)
        print(f"✅ Video reply saved to queue! ID: {item['id']}")

def handle_pinned_comment(engagement_engine: EngagementEngine):
    print("\n--- 📌 GENERATE PINNED COMMENT ---")
    topic = input("Video topic or title (optional): ").strip()
    pinned = engagement_engine.generate_pinned_comment(topic)
    print("\n" + "=" * 60)
    print("📌 RECOMMENDED PINNED COMMENT (Post & Pin immediately):")
    print(f"   \"{pinned}\"")
    print("=" * 60)

def handle_view_queue(schedule_mgr: ScheduleManager):
    print("\n--- 📅 POSTING SCHEDULE QUEUE ---")
    queue = schedule_mgr.load_queue()
    if not queue:
        print("Queue is empty! Use option 1 to generate and add scripts.")
        return

    print(f"\nTotal Posts in Queue: {len(queue)}\n")
    for idx, p in enumerate(queue, 1):
        status_emoji = "📝" if p['status'] == "SCRIPTED" else ("🎬" if p['status'] == "RECORDED" else "✅")
        print(f"[{idx}] ID: {p['id']} | {status_emoji} {p['status']} | Date: {p['scheduled_date']} @ {p['scheduled_time']}")
        print(f"     Title: {p['title']}")
        print(f"     Hook:  \"{p['hook'][:60]}...\"")
        print("-" * 65)

    action = input("\nOptions: [u]pdate status, [d]elete post, [b]ack: ").strip().lower()
    if action == 'u':
        pid = input("Enter Post ID to update: ").strip()
        print("New status: 1. SCRIPTED  2. RECORDED  3. POSTED")
        st_choice = input("Choice (1-3): ").strip()
        st_map = {"1": "SCRIPTED", "2": "RECORDED", "3": "POSTED"}
        if st_choice in st_map:
            if schedule_mgr.update_status(pid, st_map[st_choice]):
                print(f"✅ Post {pid} updated to {st_map[st_choice]}!")
            else:
                print("❌ Post ID not found.")
    elif action == 'd':
        pid = input("Enter Post ID to delete: ").strip()
        if schedule_mgr.delete_post(pid):
            print(f"✅ Post {pid} removed from queue.")
        else:
            print("❌ Post ID not found.")

def handle_view_times():
    print("\n--- ⏰ OPTIMAL TIKTOK POSTING TIMES (GAMING NICHE) ---")
    for s in PEAK_POSTING_HOURS:
        print(f"  • {s['slot']} - {s['time']}")
        print(f"    Focus: {s['niche']}")
    print("\n💡 Strategy Tip: Post 30-45 minutes before peak viewing windows so TikTok's initial test batch (200-500 views) can validate completion rate before high-traffic hours.")

def handle_launch_web():
    print("\n🌐 Starting Local Web Dashboard...")
    try:
        import subprocess
        web_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_app.py")
        print(f"Starting server at http://localhost:8080 ...")
        # Run web server
        subprocess.run([sys.executable, web_script])
    except Exception as e:
        print(f"Could not launch web server: {e}")

def main():
    content_engine = ContentEngine()
    engagement_engine = EngagementEngine()
    schedule_mgr = ScheduleManager()

    print_banner()

    while True:
        display_menu()
        choice = input("Select an option (0-7): ").strip()
        
        if choice == '1':
            handle_generate_script(content_engine, schedule_mgr)
        elif choice == '2':
            handle_comment_reply(engagement_engine)
        elif choice == '3':
            handle_video_reply(engagement_engine, schedule_mgr)
        elif choice == '4':
            handle_pinned_comment(engagement_engine)
        elif choice == '5':
            handle_view_queue(schedule_mgr)
        elif choice == '6':
            handle_view_times()
        elif choice == '7':
            handle_launch_web()
        elif choice == '0':
            print("\n👋 Good luck blowing up on TikTok! Vice City awaits.\n")
            break
        else:
            print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
