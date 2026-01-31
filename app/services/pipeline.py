from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from app.services.ffmpeg_audio import ensure_ffmpeg_available, to_clean_wav
from app.services.whisper_asr import transcribe_wav
from app.services.ollama_llm import summarize

@dataclass
class PipelineResult:
    clean_wav: Path
    transcript_path: Path
    summary_path: Path

def run_pipeline(
    input_media: Path,
    output_dir: Path,
    whisper_model: str,
    language: str,
    ollama_url: str,
    ollama_model: str,
    prompt_template: str
) -> PipelineResult:
    ensure_ffmpeg_available()

    output_dir.mkdir(parents=True, exist_ok=True)

    stem = input_media.stem
    clean_wav = output_dir / f"{stem}.clean.wav"
    transcript_file = output_dir / f"{stem}.transcript.txt"
    summary_file = output_dir / f"{stem}.summary.md"

    to_clean_wav(input_media, clean_wav)

    transcript = transcribe_wav(clean_wav, whisper_model, language)
    transcript_file.write_text(transcript, encoding="utf-8")

    prompt = prompt_template.replace("{{TRANSCRIPT}}", transcript)
    summary = summarize(ollama_url, ollama_model, prompt)

    summary_file.write_text(summary, encoding="utf-8")

    return PipelineResult(clean_wav=clean_wav, transcript_path=transcript_file, summary_path=summary_file)
