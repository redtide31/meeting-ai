from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

ALLOWED_EXTS = {".wav", ".mp3", ".m4a", ".mp4", ".mkv", ".mov", ".webm", ".flac", ".aac", ".ogg"}

@dataclass(frozen=True)
class MediaFile:
    path: Path
    size_bytes: int

def list_media_files(input_dir: Path) -> list[MediaFile]:
    if not input_dir.exists() or not input_dir.is_dir():
        return []
    files: list[MediaFile] = []
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in ALLOWED_EXTS:
            files.append(MediaFile(path=p, size_bytes=p.stat().st_size))
    return files
