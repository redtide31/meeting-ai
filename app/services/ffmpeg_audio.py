from __future__ import annotations
import subprocess
from pathlib import Path

class FFmpegError(RuntimeError):
    pass

def ensure_ffmpeg_available() -> None:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True, text=True)
    except Exception as e:
        raise FFmpegError("ffmpeg not found on PATH. Install FFmpeg and restart your terminal.") from e

def to_clean_wav(input_path: Path, output_path: Path) -> Path:
    """
    Convert to Whisper-friendly WAV:
      - mono
      - 16kHz
      - loudness normalization
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(input_path),
        "-ac", "1",
        "-ar", "16000",
        "-af", "loudnorm",
        str(output_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise FFmpegError(f"ffmpeg failed for {input_path.name}: {proc.stderr[:800]}")
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise FFmpegError(f"ffmpeg produced an empty output for {input_path.name}")
    return output_path
