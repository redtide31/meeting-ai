# 🎙️ Local Meeting AI  
**Offline Transcription & Summarization for Meetings**  
**Whisper + LLaMA 3 (Ollama) + Streamlit**

---

## Overview

**Local Meeting AI** is a **privacy-first, fully local application** that allows you to:

- Select recorded meeting audio or video files through a **web-based UI**
- Transcribe them locally using **OpenAI Whisper**
- Summarize them locally using **LLaMA 3 via Ollama**
- Store transcripts and summaries on disk
- Avoid SaaS meeting bots, browser extensions, or cloud-based processing

All processing happens **on your machine**. No data is uploaded to third-party services.

This tool is ideal for **security-conscious environments**, including:
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

