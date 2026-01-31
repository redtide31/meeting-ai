from pydantic import BaseModel, Field
from pathlib import Path

class Settings(BaseModel):
    input_dir: Path = Field(default=Path.home() / "OneDrive" / "Videos")
    output_dir: Path = Field(default=Path.home() / "meeting-ai-output")
    ollama_url: str = Field(default="http://127.0.0.1:11434")
    ollama_model: str = Field(default="llama3")
    whisper_model: str = Field(default="medium")  # large-v2 for more accuracy (slower)
    language: str = Field(default="en")
    max_file_mb: int = Field(default=2048)  # hard guardrail

settings = Settings()
