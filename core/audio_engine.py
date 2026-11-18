"""
Audio Generation Engine for GTA 6 TikTok Page Manager.
Generates voiceover narration audio for video scripts.
Supports:
1. Windows Native Speech Synthesis (System.Speech - zero dependencies, instant, built-in to Windows).
2. Edge Neural TTS (ultra-realistic viral TikTok voices if edge-tts is installed).
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "audio_exports"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

class AudioEngine:
    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or AUDIO_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_narration(self, text: str, filename_base: str, voice_style: str = "male_hype") -> Dict[str, Any]:
        """Generates voiceover audio file for a given narration text."""
        # Sanitize text
        clean_text = text.replace('"', '""').replace("'", "''").strip()
        
        # Output path
        output_wav = self.output_dir / f"{filename_base}.wav"

        # Try Edge-TTS first for ultra-realistic neural voices
        if self._try_edge_tts(clean_text, str(output_wav.with_suffix(".mp3")), voice_style):
            mp3_path = output_wav.with_suffix(".mp3")
            return {
                "success": True,
                "engine": "Edge Neural TTS",
                "file_path": str(mp3_path),
                "filename": mp3_path.name
            }

        # Reliable Native Windows Speech Synthesizer fallback (Built into Windows)
        success = self._generate_windows_sapi(clean_text, str(output_wav))
        if success:
            return {
                "success": True,
                "engine": "Windows Native SAPI (Offline)",
                "file_path": str(output_wav),
                "filename": output_wav.name
            }
        
        return {
            "success": False,
            "engine": "None",
            "file_path": "",
            "error": "Audio generation failed"
        }

    def _generate_windows_sapi(self, text: str, output_path: str) -> bool:
        """Uses Windows native System.Speech via PowerShell - 100% reliable on Windows with 0 installs."""
        escaped_text = text.replace("`", "``").replace('"', '`"').replace("$", "`$")
        escaped_out = output_path.replace("`", "``").replace('"', '`"')

        ps_script = f"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 1  # Slightly faster for high-retention TikTok pacing
$synth.SetOutputToWaveFile("{escaped_out}")
$synth.Speak("{escaped_text}")
$synth.Dispose()
"""
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        except Exception:
            return False

    def _try_edge_tts(self, text: str, output_path: str, voice_style: str) -> bool:
        """Attempts edge-tts if installed in Python environment."""
        voice_map = {
            "male_hype": "en-US-ChristopherNeural",
            "female_intense": "en-US-JennyNeural",
            "deep_narrator": "en-US-EricNeural"
        }
        voice = voice_map.get(voice_style, "en-US-ChristopherNeural")
        
        try:
            # Check if edge-tts command is available
            res = subprocess.run(
                ["edge-tts", "--voice", voice, "--text", text, "--write-media", output_path],
                capture_output=True,
                timeout=25
            )
            return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        except Exception:
            return False
