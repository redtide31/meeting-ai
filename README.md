# 🎙️ Local Meeting AI
**Offline Transcription & Summarization for Meetings**  
**Whisper + LLaMA 3 (Ollama) + Streamlit**

---

## Overview

**Local Meeting AI** is a **privacy-first, fully local application** that enables you to:

- Select recorded meeting audio or video files through a **web-based UI**
- Transcribe them locally using **OpenAI Whisper**
- Summarize them locally using **LLaMA 3 via Ollama**
- Store transcripts and summaries on disk
- Avoid SaaS meeting bots, browser extensions, or cloud-based processing

All processing happens **on your machine**. No data is uploaded to third-party services.

This tool is well-suited for **security-conscious environments**, including:
- Information Security teams  
- Legal and compliance teams  
- Executive and internal meetings  
- Research and internal documentation workflows  

---

## What This Tool Is (and Is Not)

### ✅ This tool **is**
- Fully local and self-hosted
- UI-driven (no CLI-only workflow required)
- Deterministic and auditable
- Language-aware (English, Spanish, and more)
- Safe for sensitive or regulated conversations

### ❌ This tool **is not**
- A meeting recorder (recording is done separately, e.g., OBS)
- A SaaS product
- A browser extension or meeting “bot”
- A cloud transcription service

---

## Architecture

```
Audio / Video File
        ↓
FFmpeg (normalize, mono, 16kHz)
        ↓
Whisper (local transcription)
        ↓
LLaMA 3 via Ollama (local summarization)
        ↓
Transcript (.txt) + Summary (.md)
```

---

## Requirements

### Operating System
- Windows 10 / 11 (tested)
- macOS and Linux should work with minimal changes

---

### Required Software

#### 1️⃣ Python
- **Python 3.10 or 3.11 recommended**
- Python 3.13 may cause issues with Whisper / Torch

Verify:
```powershell
python --version
```

---

#### 2️⃣ FFmpeg
Used for audio normalization and resampling.

Install (Windows):
```powershell
winget install -e --id Gyan.FFmpeg
```

Verify:
```powershell
ffmpeg -version
```

---

#### 3️⃣ Ollama
Runs LLaMA 3 locally.

Install:
- https://ollama.com/

Pull the model:
```powershell
ollama pull llama3
```

Verify:
```powershell
ollama list
```

---

#### 4️⃣ OBS (Optional, Recommended)
Used to record meetings as **audio-only WAV** files.

- https://obsproject.com/
- Configure OBS for WAV output (mono preferred)

---

## Installation

From the repository root:

### 1️⃣ Create a virtual environment
```powershell
python -m venv .venv
```

### 2️⃣ Activate it
```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks execution:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

---

### 3️⃣ Install dependencies
```powershell
pip install -U pip
pip install streamlit requests pydantic tqdm
pip install -U git+https://github.com/openai/whisper.git
```

---

## Running the Application

From the **project root directory**:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run app/ui.py
```

The UI will be available at:

```
http://localhost:8501
```

---

## How to Use the Application

### 1️⃣ Input Folder
- Select the folder containing your audio or video files
- Supported formats:
  - `.wav`, `.mp3`, `.m4a`, `.mp4`, `.mkv`, `.mov`, `.webm`, `.flac`

### 2️⃣ Output Folder
- Directory where results will be saved:
  - Cleaned WAV file
  - Transcript (`.txt`)
  - Summary (`.md`)

### 3️⃣ Whisper Model
- `small` – fastest, lowest accuracy
- `medium` – best balance (default)
- `large-v2` – highest accuracy (slower)

### 4️⃣ Language
- `en` – English
- `es` – Spanish
- Used by Whisper to bias transcription

### 5️⃣ Ollama Settings
- URL: `http://127.0.0.1:11434`
- Model: `llama3`

---

### 6️⃣ Select Files
- Choose one or more media files from the input folder
- File size limits are enforced to prevent runaway processing

### 7️⃣ Run Pipeline
Click **“Transcribe + Summarize”**

Progress is displayed per file.

---

## Output Files

For each processed file:

```
<filename>.clean.wav        # Normalized, mono, 16kHz audio
<filename>.transcript.txt   # Whisper transcription
<filename>.summary.md       # LLaMA 3 summary (Markdown)
```

---

## Language Support

### Transcription
- Whisper supports multilingual input
- Explicitly set the language for best accuracy

### Summarization
- The summary language is controlled by the prompt template

To force Spanish summaries, edit:
```
app/prompts/summary.txt
```

Example:
```text
IMPORTANTE:
- Responde completamente en español
```

Restart the app after modifying prompts.

---

## Testing

Install development dependencies:
```powershell
pip install -e "[dev]"
```

Run tests:
```powershell
pytest
```

Tests cover:
- File discovery
- FFmpeg availability
- Ollama error handling
- Pipeline failure behavior

---

## Security & Privacy

- No cloud transcription
- No meeting bots or browser extensions
- No external APIs (except local Ollama)
- Files remain on disk at all times

This design is appropriate for:
- Sensitive corporate meetings
- Legal or compliance-related discussions
- Security and research workflows

---

## Common Issues

### `ModuleNotFoundError: No module named 'app'`
Run Streamlit with the project root on `PYTHONPATH`:
```powershell
$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run app/ui.py
```

---

### Ollama connection errors
Ensure Ollama is running:
```powershell
ollama list
```

---

### Poor transcription quality
- Prefer WAV recordings
- Ensure mono audio
- Use `large-v2` Whisper model if resources allow

---

## Roadmap (Optional Enhancements)

- Speaker diarization
- Automatic language detection
- Background job queue
- Docker deployment
- Cryptographic hashes for audit trails

---

## License

Add your preferred license (e.g., MIT, Apache 2.0).

