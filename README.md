# 🌴 GTA 6 TikTok Page Manager & Engagement Engine

An all-in-one content management, viral script generation, and community engagement automation tool built specifically for a **GTA 6 (Grand Theft Auto VI)** TikTok page.

---

## 🚀 Key Features

### 1. 🎬 Viral TikTok Script Studio
- **0-3s Explosive Hooks**: Tailored to stop the infinite scroll immediately.
- **Visual & B-Roll Directives**: Timed scene-by-scene clip instructions (trailer timestamps, leaked patent schematics, Florida comparisons).
- **Voiceover Narration**: Punchy 20-30 second scripts optimized for TikTok's completion rate algorithm.
- **Debate-Driven Calls-To-Action (CTAs)**: Specifically prompts viewers to flood the comments.
- **Strategic Captions & Tags**: Optimized with `#GTA6 #GTAVI #ViceCity #RockstarGames`.

### 2. 💬 Comment Engagement & Algorithm Magnet
TikTok favors videos that have high comment velocity. This tool provides **3 distinct reply styles** for any viewer comment:
1. **🧲 Engagement Magnet**: Asks a counter-question to force a reply chain.
2. **😂 Witty / Banter**: Fast-paced gamer humor & Florida Man vibes.
3. **🧠 Lore Expert**: Analytical, referencing real Rockstar patents and trailer frames.
4. **🎥 Comment-to-Video Converter**: Automatically generates a *"Replying to @user"* video script to ride high-performing comment threads.

### 3. 📅 Posting Queue & Optimal Timing
- Built-in queue tracking (`SCRIPTED` ➔ `RECORDED` ➔ `POSTED`).
- Pre-configured with the **4 Peak Gaming Windows on TikTok**:
  - `11:30 AM` - Morning Hype Drop (leaks, news, investor call updates)
  - `03:30 PM` - Afternoon Rush (breakdowns, easter eggs, comparisons)
  - `07:00 PM` - Prime Time Peak (theories, story debates, map scale)
  - `09:30 PM` - Late Night Viral (memes, Florida Man, countdown polls)

### 4. 🌐 Web Dashboard + Terminal CLI
- **Interactive Web App**: Neon Vice City UI running locally at `http://localhost:8080` (pure Python, zero dependencies required).
- **Interactive CLI**: Quick terminal interface for power users.

---

## 🛠️ Quick Start

### 1. Open the Project
```bash
cd C:\Users\SmartKid\.gemini\antigravity\scratch\gta6-tiktok-manager
```

### 2. Run the Interactive Web Dashboard
```bash
python web_app.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser!

### 3. Or Run the Command-Line Interface
```bash
python manager.py
```

---

## 🤖 Optional: Gemini AI Integration
The manager works **100% offline** using built-in algorithmic GTA 6 templates and formulas.
If you want dynamic AI-generated scripts on any custom topic:
```bash
set GEMINI_API_KEY=your_gemini_api_key
pip install google-genai
```

---

## 📁 Project Structure
```
gta6-tiktok-manager/
├── manager.py                # Command-line interface
├── web_app.py                # Local web dashboard (http://localhost:8080)
├── config.py                 # Configuration & time slots
├── requirements.txt          # Optional dependencies
├── README.md                 # Documentation
├── core/
│   ├── ai_client.py          # Gemini AI + offline heuristic engine
│   ├── content_engine.py     # Script builder & pillar manager
│   ├── engagement_engine.py  # Comment replier & video reply generator
│   ├── schedule_manager.py   # Post queue & calendar manager
│   └── templates.py          # Curated viral GTA 6 hooks & scripts
└── data/
    ├── gta6_knowledge.json   # Verified GTA 6 facts, locations & lore
    ├── posts_queue.json      # Your scheduled video pipeline
    └── engagement_log.json   # Record of comments handled
```
