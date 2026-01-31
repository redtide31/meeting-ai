from __future__ import annotations
from pathlib import Path
import whisper

class TranscriptionError(RuntimeError):
    pass

def transcribe_wav(wav_path: Path, model_name: str, language: str) -> str:
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(str(wav_path), language=language, fp16=False, temperature=0)
        text = (result.get("text") or "").strip()
        if not text:
            raise TranscriptionError("Whisper returned empty transcript.")
        return text
    except Exception as e:
        raise TranscriptionError(f"Whisper failed: {e}") from e
