"""
GTA 6 TikTok Page Manager - Sleek Local Web Dashboard.
Runs on Python standard library (http.server) with no external web dependencies needed.
Run: python web_app.py
Access at: http://localhost:8080
"""
import sys
import os
import json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Ensure local imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONTENT_PILLARS, PEAK_POSTING_HOURS, ACCOUNT_TONES
from core.content_engine import ContentEngine
from core.engagement_engine import EngagementEngine
from core.schedule_manager import ScheduleManager

PORT = int(os.environ.get("PORT", 8080))

content_engine = ContentEngine()
engagement_engine = EngagementEngine()
schedule_mgr = ScheduleManager()

HTML_DASHBOARD = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GTA 6 TikTok Page Manager</title>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #0a0614;
      --bg-card: #130c24;
      --bg-card-hover: #1c1236;
      --neon-pink: #ff2a85;
      --neon-cyan: #00f0ff;
      --neon-purple: #9d4edd;
      --neon-yellow: #ffd60a;
      --text-main: #f0f2f8;
      --text-muted: #9ba1b9;
      --border: #281a4d;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Montserrat', sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Header & Branding */
    header {
      background: linear-gradient(135deg, #160a33 0%, #0d061e 100%);
      border-bottom: 2px solid var(--neon-pink);
      padding: 1.2rem 2.5rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 25px rgba(255, 42, 133, 0.15);
    }
    .logo-container h1 {
      font-size: 1.8rem;
      font-weight: 900;
      letter-spacing: 1px;
      background: linear-gradient(90deg, var(--neon-pink), #ff70a6, var(--neon-cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      text-transform: uppercase;
    }
    .logo-container p {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .badge {
      background: rgba(0, 240, 255, 0.12);
      border: 1px solid var(--neon-cyan);
      color: var(--neon-cyan);
      font-size: 0.75rem;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 20px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    /* Navigation Tabs */
    .tabs {
      display: flex;
      gap: 12px;
      padding: 1rem 2.5rem;
      background: #0f0820;
      border-bottom: 1px solid var(--border);
    }
    .tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 10px 20px;
      font-weight: 700;
      font-size: 0.9rem;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .tab-btn:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.05);
    }
    .tab-btn.active {
      background: rgba(255, 42, 133, 0.15);
      border-color: var(--neon-pink);
      color: var(--neon-pink);
      box-shadow: 0 0 15px rgba(255, 42, 133, 0.3);
    }

    /* Main Container */
    main {
      flex: 1;
      padding: 2rem 2.5rem;
      max-width: 1400px;
      width: 100%;
      margin: 0 auto;
    }

    .tab-content { display: none; }
    .tab-content.active { display: block; animation: fadeIn 0.3s ease; }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Grid Layouts */
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    @media (max-width: 900px) {
      .grid-2 { grid-template-columns: 1fr; }
    }

    /* Cards */
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 1.8rem;
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
      position: relative;
    }
    .card-title {
      font-size: 1.2rem;
      font-weight: 800;
      margin-bottom: 1.2rem;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    /* Form Controls */
    .form-group {
      margin-bottom: 1.2rem;
    }
    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    input, select, textarea {
      width: 100%;
      background: #090412;
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 12px 14px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 0.95rem;
      transition: border-color 0.2s;
    }
    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--neon-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    textarea { resize: vertical; min-height: 100px; }

    /* Buttons */
    .btn {
      background: linear-gradient(135deg, var(--neon-pink), #e01e74);
      color: #fff;
      border: none;
      padding: 12px 24px;
      font-weight: 800;
      font-size: 0.95rem;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 4px 15px rgba(255, 42, 133, 0.4);
    }
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(255, 42, 133, 0.6);
    }
    .btn-secondary {
      background: #1e1338;
      border: 1px solid var(--neon-purple);
      color: var(--text-main);
      box-shadow: none;
    }
    .btn-secondary:hover {
      background: #2b1b4f;
      border-color: var(--neon-cyan);
      transform: translateY(-2px);
    }
    .btn-sm {
      padding: 6px 12px;
      font-size: 0.8rem;
    }

    /* Output Sections */
    .output-box {
      background: #090514;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.2rem;
      margin-top: 1rem;
    }
    .script-section {
      margin-bottom: 1.2rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid #1f143d;
    }
    .script-section:last-child { border-bottom: none; margin-bottom: 0; padding-bottom: 0; }
    .section-label {
      font-size: 0.75rem;
      font-weight: 800;
      color: var(--neon-cyan);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 4px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .section-text {
      font-size: 0.95rem;
      line-height: 1.5;
      color: #e5e8f4;
    }
    .code-box {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.88rem;
      background: #06030c;
      padding: 10px 14px;
      border-radius: 6px;
      border-left: 3px solid var(--neon-pink);
      color: #92e0ff;
      margin-top: 4px;
    }

    /* Reply Cards */
    .reply-card {
      background: #0d071a;
      border: 1px solid #231642;
      border-radius: 8px;
      padding: 1rem;
      margin-bottom: 12px;
      transition: border-color 0.2s;
    }
    .reply-card:hover { border-color: var(--neon-cyan); }
    .reply-tag {
      font-size: 0.7rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      display: inline-block;
      margin-bottom: 6px;
    }
    .tag-magnet { background: rgba(0, 240, 255, 0.15); color: var(--neon-cyan); border: 1px solid var(--neon-cyan); }
    .tag-witty { background: rgba(255, 214, 10, 0.15); color: var(--neon-yellow); border: 1px solid var(--neon-yellow); }
    .tag-lore { background: rgba(157, 78, 221, 0.15); color: var(--neon-purple); border: 1px solid var(--neon-purple); }

    /* Post Queue Table */
    .queue-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1rem;
    }
    .queue-table th {
      text-align: left;
      padding: 12px 14px;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
    }
    .queue-table td {
      padding: 14px;
      border-bottom: 1px solid #1a1036;
      font-size: 0.9rem;
    }
    .status-badge {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 0.75rem;
      font-weight: 800;
    }
    .status-SCRIPTED { background: rgba(0, 240, 255, 0.15); color: var(--neon-cyan); border: 1px solid var(--neon-cyan); }
    .status-RECORDED { background: rgba(255, 214, 10, 0.15); color: var(--neon-yellow); border: 1px solid var(--neon-yellow); }
    .status-POSTED { background: rgba(46, 204, 113, 0.15); color: #2ecc71; border: 1px solid #2ecc71; }

    /* Copy Button */
    .btn-copy {
      background: transparent;
      border: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.75rem;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
    }
    .btn-copy:hover { color: var(--neon-cyan); border-color: var(--neon-cyan); }

    .schedule-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-top: 1rem;
    }
    .slot-box {
      background: #0d061e;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.2rem;
      border-top: 3px solid var(--neon-pink);
    }
    .slot-box h4 { color: var(--neon-cyan); font-size: 1rem; margin-bottom: 4px; }
    .slot-time { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: var(--neon-yellow); font-weight: 700; margin-bottom: 8px; }
    .slot-desc { font-size: 0.85rem; color: var(--text-muted); }
  </style>
</head>
<body>

  <header>
    <div class="logo-container">
      <h1>🌴 GTA 6 TikTok Page Manager</h1>
      <p>Automated Script Blueprints, Viral Hooks & Community Engagement Engine</p>
    </div>
    <div class="badge">Vice City Edition • 2026 Ready</div>
  </header>

  <div class="tabs">
    <button class="tab-btn active" onclick="switchTab('tab-scripts')">🎬 Script Studio</button>
    <button class="tab-btn" onclick="switchTab('tab-engagement')">💬 Comment Engager</button>
    <button class="tab-btn" onclick="switchTab('tab-queue')">📅 Posting Queue</button>
    <button class="tab-btn" onclick="switchTab('tab-strategy')">⏰ Optimal Times & Strategy</button>
  </div>

  <main>
    <!-- TAB 1: SCRIPT STUDIO -->
    <div id="tab-scripts" class="tab-content active">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">✨ Generate New TikTok Blueprint</div>
          
          <div class="form-group">
            <label>Content Pillar</label>
            <select id="script-pillar">
              <option value="">-- Random / Surprise Me --</option>
              <option value="Trailer & Teaser Breakdowns">Trailer & Teaser Breakdowns</option>
              <option value="Hidden Easter Eggs & Map Details">Hidden Easter Eggs & Map Details</option>
              <option value="Lucia & Jason Dynamics & Theories">Lucia & Jason Dynamics & Theories</option>
              <option value="Rockstar Technology, AI & Leaks">Rockstar Technology, AI & Leaks</option>
              <option value="Real Florida vs. Leonida Comparisons">Real Florida vs. Leonida Comparisons</option>
              <option value="Release Date Rumors & Take-Two Updates">Release Date Rumors & Take-Two Updates</option>
              <option value="Community Debates & Comment Video Replies">Community Debates & Video Replies</option>
            </select>
          </div>

          <div class="form-group">
            <label>Specific Topic or Angle (Optional)</label>
            <input type="text" id="script-topic" placeholder="e.g. Lucia's ankle monitor, hurricane water physics, map size">
          </div>

          <div class="form-group">
            <label>Account Tone</label>
            <select id="script-tone">
              <option value="hype">Excited Gamer Hype (Fast-paced)</option>
              <option value="lore_expert">Analytical Lore Researcher (Deep detail)</option>
              <option value="satirical">Florida Man Humor & Memes</option>
              <option value="debate_provoker">Debate Provoker (Maximizes comments)</option>
            </select>
          </div>

          <button class="btn" onclick="generateScript()" id="gen-btn">⚡ Generate Viral Blueprint</button>
        </div>

        <div class="card">
          <div class="card-title">
            <span>📋 Generated Script Output</span>
            <button class="btn btn-secondary btn-sm" id="add-queue-btn" style="display:none;" onclick="addCurrentToQueue()">➕ Add to Queue</button>
          </div>

          <div id="script-result-placeholder" style="color: var(--text-muted); padding: 2rem; text-align: center;">
            Click <strong>Generate Viral Blueprint</strong> to produce a complete TikTok hook, visual cues, voiceover script, and caption.
          </div>

          <div id="script-result" style="display: none;" class="output-box">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 2: COMMENT ENGAGER -->
    <div id="tab-engagement" class="tab-content">
      <div class="grid-2">
        <div class="card">
          <div class="card-title">💬 Comment Reply & Viral Retargeting</div>
          
          <div class="form-group">
            <label>Paste Viewer's Comment</label>
            <textarea id="comment-input" placeholder="e.g. 'This game is definitely getting delayed to 2027 lol' or 'Is Lucia going to betray Jason?'"></textarea>
          </div>

          <div style="display: flex; gap: 10px;">
            <button class="btn" onclick="generateReplies()">🧲 Generate 3 Viral Replies</button>
            <button class="btn btn-secondary" onclick="generateVideoReply()">🎥 Turn into Video Script</button>
          </div>

          <hr style="border: none; border-top: 1px solid var(--border); margin: 1.5rem 0;">

          <div class="card-title">📌 Instant Pinned Comment Generator</div>
          <div class="form-group">
            <label>Post Topic (Optional)</label>
            <input type="text" id="pinned-topic" placeholder="e.g. First car to steal, Jason vs Lucia">
          </div>
          <button class="btn btn-secondary" onclick="generatePinnedComment()">🔥 Generate Pinned Comment</button>
          <div id="pinned-result" style="margin-top: 10px;"></div>
        </div>

        <div class="card">
          <div class="card-title">🎯 Algorithmic Engagement Replies</div>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem;">
            Replying with questions or provocative counter-points forces the viewer to comment back, driving up the video's engagement score in TikTok's algorithm.
          </p>

          <div id="replies-placeholder" style="color: var(--text-muted); padding: 2rem; text-align: center;">
            Paste a comment on the left to see 3 specialized reply strategies.
          </div>

          <div id="replies-container" style="display: none;">
            <!-- Populated via JS -->
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: POSTING QUEUE -->
    <div id="tab-queue" class="tab-content">
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <div class="card-title" style="margin-bottom: 0;">📅 Scheduled Post Queue</div>
          <button class="btn btn-secondary btn-sm" onclick="loadQueue()">🔄 Refresh Queue</button>
        </div>

        <div style="overflow-x: auto;">
          <table class="queue-table">
            <thead>
              <tr>
                <th>Date & Slot</th>
                <th>Title & Pillar</th>
                <th>Hook Preview</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="queue-tbody">
              <!-- Populated via JS -->
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 4: OPTIMAL TIMES & STRATEGY -->
    <div id="tab-strategy" class="tab-content">
      <div class="card">
        <div class="card-title">⏰ Peak TikTok Posting Windows for GTA 6 / Gaming</div>
        <p style="color: var(--text-muted); font-size: 0.9rem;">
          Gaming audiences peak during mid-day lunch breaks and post-school/work evening hours. Aim to post 30 minutes before these windows.
        </p>
        
        <div class="schedule-grid">
          <div class="slot-box">
            <h4>Morning Hype Drop</h4>
            <div class="slot-time">11:30 AM</div>
            <div class="slot-desc">Best for: Fast news, short leaks, Take-Two financial hints, and morning updates.</div>
          </div>
          <div class="slot-box">
            <h4>Afternoon Rush</h4>
            <div class="slot-time">03:30 PM</div>
            <div class="slot-desc">Best for: Trailer breakdowns, Easter egg zooms, and visual graphic comparisons.</div>
          </div>
          <div class="slot-box" style="border-top-color: var(--neon-cyan);">
            <h4>Prime Time Peak ⭐</h4>
            <div class="slot-time">07:00 PM</div>
            <div class="slot-desc">Best for: Deep story theories (Lucia/Jason), betrayal debates, and map investigations. Highest comment rate!</div>
          </div>
          <div class="slot-box" style="border-top-color: var(--neon-yellow);">
            <h4>Late Night Viral</h4>
            <div class="slot-time">09:30 PM</div>
            <div class="slot-desc">Best for: Florida Man unhinged humor, relatable memes, GTA 6 countdowns, and polls.</div>
          </div>
        </div>

        <hr style="border: none; border-top: 1px solid var(--border); margin: 2rem 0;">

        <div class="card-title">🚀 The 3-Step GTA 6 TikTok Growth Playbook</div>
        <div class="grid-2" style="margin-top: 1rem;">
          <div style="background: #090412; padding: 1.2rem; border-radius: 8px; border: 1px solid var(--border);">
            <h4 style="color: var(--neon-pink); margin-bottom: 6px;">1. The 3-Second Rule</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Never say "Hey guys welcome back". Start directly with the punchline: <em>"Rockstar secretly hid this at 0:34..."</em>. Use high-contrast bold yellow/white captions.
            </p>
          </div>
          <div style="background: #090412; padding: 1.2rem; border-radius: 8px; border: 1px solid var(--border);">
            <h4 style="color: var(--neon-cyan); margin-bottom: 6px;">2. Pinned Comment Controversy</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Immediately pin a provocative comment asking a 50/50 debate (e.g. <em>"Play today at 30 FPS OR wait 1 year for 60 FPS?"</em>). This triggers 100+ comments within 15 minutes.
            </p>
          </div>
          <div style="background: #090412; padding: 1.2rem; border-radius: 8px; border: 1px solid var(--border);">
            <h4 style="color: var(--neon-purple); margin-bottom: 6px;">3. Video Reply Snowball</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              When a comment gets over 20 likes, tap "Reply with video". TikTok rewards video replies with algorithmic bonus distribution because it indicates a thriving community.
            </p>
          </div>
          <div style="background: #090412; padding: 1.2rem; border-radius: 8px; border: 1px solid var(--border);">
            <h4 style="color: var(--neon-yellow); margin-bottom: 6px;">4. Audio Hijacking</h4>
            <p style="font-size: 0.88rem; color: var(--text-muted);">
              Keep the official trailer song ("Love Is a Long Road") or trending phonk audio set to 3-5% volume under your voiceover so TikTok categorizes your video under the trending sound.
            </p>
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    let currentScript = null;

    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById(tabId).classList.add('active');
      if (tabId === 'tab-queue') loadQueue();
    }

    async function generateScript() {
      const pillar = document.getElementById('script-pillar').value;
      const topic = document.getElementById('script-topic').value;
      const tone = document.getElementById('script-tone').value;
      const btn = document.getElementById('gen-btn');
      
      btn.innerText = "⏳ Generating Blueprint...";
      btn.disabled = true;

      try {
        const res = await fetch('/api/generate-script', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ pillar, topic, tone })
        });
        const data = await res.json();
        currentScript = data;
        renderScript(data);
        document.getElementById('add-queue-btn').style.display = 'inline-flex';
      } catch (err) {
        alert("Error generating script: " + err);
      } finally {
        btn.innerText = "⚡ Generate Viral Blueprint";
        btn.disabled = false;
      }
    }

    function renderScript(s) {
      document.getElementById('script-result-placeholder').style.display = 'none';
      const container = document.getElementById('script-result');
      container.style.display = 'block';

      let cuesHtml = (s.visual_cues || []).map(c => `<li>${c}</li>`).join('');

      container.innerHTML = `
        <div class="script-section">
          <div class="section-label">
            <span>⚡ Explosive Hook (0-3s)</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(s.hook)}')">Copy</button>
          </div>
          <div class="code-box">${s.hook}</div>
        </div>

        <div class="script-section">
          <div class="section-label">
            <span>🎥 Visual Cues / B-Roll Instructions</span>
          </div>
          <ul style="padding-left: 20px; font-size: 0.88rem; color: #b4bacf; line-height: 1.6;">
            ${cuesHtml}
          </ul>
        </div>

        <div class="script-section">
          <div class="section-label">
            <span>🎙️ Full Narration (20-30s)</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(s.narration)}')">Copy</button>
          </div>
          <div class="section-text" style="background: #110924; padding: 10px; border-radius: 6px; border-left: 3px solid var(--neon-cyan);">
            ${s.narration}
          </div>
        </div>

        <div class="script-section">
          <div class="section-label">
            <span>📢 High-Retention CTA</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(s.cta)}')">Copy</button>
          </div>
          <div class="section-text" style="color: var(--neon-yellow);">${s.cta}</div>
        </div>

        <div class="script-section">
          <div class="section-label">
            <span>📝 Caption & Viral Hashtags</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(s.caption)}')">Copy</button>
          </div>
          <div class="code-box" style="border-left-color: var(--neon-purple);">${s.caption}</div>
        </div>

        <div class="script-section">
          <div class="section-label">
            <span>📌 Pinned Comment to Post</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(s.pinned_comment)}')">Copy</button>
          </div>
          <div class="section-text" style="font-weight: 600; color: #00f0ff;">${s.pinned_comment}</div>
        </div>
      `;
    }

    async function addCurrentToQueue() {
      if (!currentScript) return;
      try {
        const res = await fetch('/api/add-to-queue', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ video_data: currentScript })
        });
        const data = await res.json();
        alert(`✅ Script added to posting schedule! [Post ID: ${data.id}]`);
      } catch (err) {
        alert("Error adding to queue: " + err);
      }
    }

    async function generateReplies() {
      const comment = document.getElementById('comment-input').value.trim();
      if (!comment) { alert("Please paste a comment first!"); return; }

      const res = await fetch('/api/generate-reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment })
      });
      const data = await res.json();

      document.getElementById('replies-placeholder').style.display = 'none';
      const container = document.getElementById('replies-container');
      container.style.display = 'block';

      container.innerHTML = `
        <div class="reply-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="reply-tag tag-magnet">🧲 Engagement Magnet (Forces Response)</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(data.engagement_magnet)}')">Copy</button>
          </div>
          <div style="margin-top: 6px; font-size: 0.95rem;">${data.engagement_magnet}</div>
        </div>

        <div class="reply-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="reply-tag tag-witty">😂 Witty Banter (Viral Gamer Tone)</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(data.witty_banter)}')">Copy</button>
          </div>
          <div style="margin-top: 6px; font-size: 0.95rem;">${data.witty_banter}</div>
        </div>

        <div class="reply-card">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="reply-tag tag-lore">🧠 Lore Expert (Rockstar Factual)</span>
            <button class="btn-copy" onclick="copyText('${escapeQuotes(data.lore_expert)}')">Copy</button>
          </div>
          <div style="margin-top: 6px; font-size: 0.95rem;">${data.lore_expert}</div>
        </div>
      `;
    }

    async function generateVideoReply() {
      const comment = document.getElementById('comment-input').value.trim();
      if (!comment) { alert("Please paste a comment first!"); return; }

      const res = await fetch('/api/generate-video-reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comment, username: "@viewer" })
      });
      const data = await res.json();
      currentScript = data;
      switchTab('tab-scripts');
      renderScript(data);
      document.getElementById('add-queue-btn').style.display = 'inline-flex';
    }

    async function generatePinnedComment() {
      const topic = document.getElementById('pinned-topic').value;
      const res = await fetch('/api/generate-pinned', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      const data = await res.json();
      document.getElementById('pinned-result').innerHTML = `
        <div class="code-box" style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
          <span>${data.pinned_comment}</span>
          <button class="btn-copy" onclick="copyText('${escapeQuotes(data.pinned_comment)}')">Copy</button>
        </div>
      `;
    }

    async function loadQueue() {
      const tbody = document.getElementById('queue-tbody');
      tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Loading queue...</td></tr>';
      
      const res = await fetch('/api/queue');
      const queue = await res.json();

      if (!queue || queue.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">No posts in queue yet! Generate a script and click "Add to Queue".</td></tr>';
        return;
      }

      tbody.innerHTML = queue.map(p => `
        <tr>
          <td>
            <strong>${p.scheduled_date}</strong><br>
            <span style="font-size: 0.8rem; color: var(--neon-yellow);">${p.scheduled_time} (${p.slot_name})</span>
          </td>
          <td>
            <strong>${p.title}</strong><br>
            <span style="font-size: 0.75rem; color: var(--text-muted);">${p.pillar}</span>
          </td>
          <td style="max-width: 300px; font-size: 0.85rem; color: #c4c8db;">"${p.hook}"</td>
          <td><span class="status-badge status-${p.status}">${p.status}</span></td>
          <td>
            <div style="display: flex; gap: 6px;">
              ${p.status !== 'POSTED' ? `<button class="btn-copy" onclick="updatePostStatus('${p.id}', 'POSTED')">Mark Posted</button>` : ''}
              <button class="btn-copy" style="color: #ff4757;" onclick="deletePost('${p.id}')">Delete</button>
            </div>
          </td>
        </tr>
      `).join('');
    }

    async function updatePostStatus(id, newStatus) {
      await fetch('/api/update-status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status: newStatus })
      });
      loadQueue();
    }

    async function deletePost(id) {
      if (!confirm("Remove this post from queue?")) return;
      await fetch('/api/delete-post', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id })
      });
      loadQueue();
    }

    function escapeQuotes(str) {
      if (!str) return '';
      return str.replace(/'/g, "\\'").replace(/"/g, '&quot;');
    }

    function copyText(txt) {
      navigator.clipboard.writeText(txt);
      alert("Copied to clipboard!");
    }
  </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length > 0:
            return json.loads(self.rfile.read(content_length).decode("utf-8"))
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_DASHBOARD.encode("utf-8"))
        elif parsed.path == "/api/queue":
            self._send_json(schedule_mgr.load_queue())
        elif parsed.path == "/api/posting-times":
            self._send_json(PEAK_POSTING_HOURS)
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        body = self._read_body()

        if parsed.path == "/api/generate-script":
            pillar = body.get("pillar", "")
            topic = body.get("topic", "")
            tone = body.get("tone", "hype")
            script = content_engine.create_video_script(topic=topic, pillar=pillar, tone=tone)
            self._send_json(script)

        elif parsed.path == "/api/generate-reply":
            comment = body.get("comment", "")
            replies = engagement_engine.get_comment_replies(comment)
            self._send_json(replies)

        elif parsed.path == "/api/generate-video-reply":
            comment = body.get("comment", "")
            user = body.get("username", "@viewer")
            video_pkg = engagement_engine.comment_to_video_reply_concept(username=user, comment_text=comment)
            self._send_json(video_pkg)

        elif parsed.path == "/api/generate-pinned":
            topic = body.get("topic", "")
            pinned = engagement_engine.generate_pinned_comment(topic)
            self._send_json({"pinned_comment": pinned})

        elif parsed.path == "/api/add-to-queue":
            video_data = body.get("video_data", {})
            scheduled_date = body.get("scheduled_date")
            slot_name = body.get("slot_name", "Prime Time Peak")
            item = schedule_mgr.add_to_queue(video_data, scheduled_date=scheduled_date, slot_name=slot_name)
            self._send_json(item)

        elif parsed.path == "/api/update-status":
            post_id = body.get("id")
            new_status = body.get("status")
            success = schedule_mgr.update_status(post_id, new_status)
            self._send_json({"success": success})

        elif parsed.path == "/api/delete-post":
            post_id = body.get("id")
            success = schedule_mgr.delete_post(post_id)
            self._send_json({"success": success})

        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = ThreadingHTTPServer(server_address, RequestHandler)
    print("=" * 65)
    print(f"🌴 GTA 6 TikTok Page Manager Dashboard is running!")
    print(f"👉 Open in browser: http://localhost:{PORT}")
    print("=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
