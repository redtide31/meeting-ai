🎙️ Local Meeting AI

Offline Meeting Recording, Transcription & Summarization
Whisper + LLaMA 3 (via Ollama) + Streamlit UI

Overview

Local Meeting AI is a fully local, self-hosted application that allows you to:

Select recorded meeting audio/video files via a web UI

Transcribe them locally using OpenAI Whisper

Summarize them locally using LLaMA 3 via Ollama

Store transcripts and summaries on disk

Avoid SaaS meeting bots, browser extensions, or cloud processing

This tool is designed for security-conscious, privacy-first workflows (InfoSec, legal, executive, research, internal operations).

No data leaves your machine.

What This Tool Is (and Is Not)
✅ This tool is

Fully local (offline once dependencies are installed)

UI-driven (no CLI knowledge required to operate)

Deterministic and auditable

Safe for sensitive or regulated conversations

Language-aware (supports English, Spanish, and more)

❌ This tool is not

A meeting recorder (recording is done separately, e.g. OBS)

A SaaS product

A browser extension

A cloud transcription service

Architecture
Audio / Video File
        ↓
FFmpeg (normalize, mono, 16kHz)
        ↓
Whisper (local transcription)
        ↓
LLaMA 3 via Ollama (local summarization)
        ↓
Transcript + Summary (saved to disk)

Requirements
Operating System

Windows 10/11 (tested)

macOS / Linux should work with minimal changes

Required Software
1️⃣ Python

Python 3.10 – 3.11 recommended

Python 3.13 may cause issues with Whisper/Torch

Verify:

python --version

2️⃣ FFmpeg

Required for audio preprocessing.

Install (Windows):

winget install -e --id Gyan.FFmpeg


Verify:

ffmpeg -version

3️⃣ Ollama

Used to run LLaMA 3 locally.

Install:

https://ollama.com/

Pull model:

ollama pull llama3


Verify:

ollama list

4️⃣ OBS (Optional, but recommended)

Used to record meetings as WAV audio.

https://obsproject.com/

Configure for audio-only WAV recording

Installation

From the repository root:

1️⃣ Create virtual environment
python -m venv .venv

2️⃣ Activate it
.\.venv\Scripts\Activate.ps1


(If blocked)

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

3️⃣ Install dependencies
pip install -U pip
pip install streamlit requests pydantic tqdm
pip install -U git+https://github.com/openai/whisper.git

Running the Application

From the project root:

$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run app/ui.py


The UI will open automatically at:

http://localhost:8501

How to Use the UI
1️⃣ Input Folder

Set the folder containing your audio/video files

Supported formats:

.wav, .mp3, .m4a, .mp4, .mkv, .mov, .webm, .flac

2️⃣ Output Folder

Where processed files will be saved:

Clean WAV

Transcript (.txt)

Summary (.md)

3️⃣ Whisper Model

small → fast, lower accuracy

medium → best balance (default)

large-v2 → highest accuracy (slower)

4️⃣ Language

en → English

es → Spanish

Whisper uses this to bias transcription

5️⃣ Ollama Settings

URL: http://127.0.0.1:11434

Model: llama3

6️⃣ Select Files

Choose one or more media files

File size guardrails are enforced

7️⃣ Run Pipeline

Click “Transcribe + Summarize”

Progress is shown per file.

Output Files

For each input file:

<filename>.clean.wav        # normalized, mono, 16kHz
<filename>.transcript.txt   # Whisper output
<filename>.summary.md       # LLaMA 3 summary

Language Support (Important)
Transcription

Whisper supports multilingual input

Set the language explicitly for best results

Summarization

The summary language is controlled by the prompt

To force Spanish output, update:

app/prompts/summary.txt


Example:

IMPORTANTE:
- Responde completamente en español


Restart the app after changing prompts.

Testing

Install dev dependencies:

pip install -e ".[dev]"


Run tests:

pytest


Tests validate:

File discovery

FFmpeg availability

Ollama error handling

Pipeline failure behavior

Security & Privacy Notes

No network calls except to local Ollama

No browser extensions

No meeting bots

No cloud uploads

Files never leave your machine

This design is suitable for:

Security teams

Legal teams

Executive meetings

Internal corporate use

Sensitive or regulated environments

Common Issues
ModuleNotFoundError: app

Fix:

$env:PYTHONPATH = (Get-Location).Path
python -m streamlit run app/ui.py

Ollama connection error

Ensure Ollama is running:

ollama list

Poor transcription quality

Use WAV audio

Ensure mono, 16kHz (handled automatically)

Switch Whisper model to large-v2

Roadmap / Extensions (Optional)

Speaker diarization

Bilingual auto-detection

Job queue / background processing

Docker packaging

Audit hashes for outputs
