from __future__ import annotations
import logging
from pathlib import Path

import streamlit as st

from app.config import settings
from app.logging_config import configure_logging
from app.services.file_scan import list_media_files
from app.services.pipeline import run_pipeline
from app.services.ollama_llm import OllamaError
from app.services.ffmpeg_audio import FFmpegError
from app.services.whisper_asr import TranscriptionError

log = logging.getLogger("meeting-ai")

def read_prompt_template() -> str:
    p = Path(__file__).parent / "prompts" / "summary.txt"
    return p.read_text(encoding="utf-8")

def main() -> None:
    configure_logging()
    st.set_page_config(page_title="Local Meeting AI", layout="wide")

    st.title("Local Meeting AI: Whisper → Llama3")
    st.caption("Local transcription + summarization. No SaaS. Files stay on disk.")

    with st.sidebar:
        st.header("Settings")
        input_dir = Path(st.text_input("Input folder", str(settings.input_dir)))
        output_dir = Path(st.text_input("Output folder", str(settings.output_dir)))
        whisper_model = st.selectbox("Whisper model", ["small", "medium", "large-v2"], index=1)
        language = st.text_input("Language", settings.language)
        ollama_url = st.text_input("Ollama URL", settings.ollama_url)
        ollama_model = st.text_input("Ollama model", settings.ollama_model)
        st.divider()
        st.write("Best practice: convert → mono 16kHz + loudnorm before Whisper (done automatically).")

    prompt_template = read_prompt_template()
    st.subheader("Select files to process")

    files = list_media_files(input_dir)
    if not files:
        st.warning("No media files found. Confirm the input folder path.")
        return

    file_labels = [f"{f.path.name} ({round(f.size_bytes/1024/1024, 1)} MB)" for f in files]
    selected = st.multiselect("Files", options=file_labels)

    selected_paths = [files[file_labels.index(lbl)].path for lbl in selected]

    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Run")
        if st.button("Transcribe + Summarize", type="primary", disabled=(len(selected_paths) == 0)):
            for p in selected_paths:
                size_mb = p.stat().st_size / 1024 / 1024
                if size_mb > settings.max_file_mb:
                    st.error(f"Skipping {p.name}: file too large ({size_mb:.1f} MB).")
                    continue

                st.write(f"Processing: **{p.name}**")
                prog = st.progress(0)

                try:
                    prog.progress(10)
                    result = run_pipeline(
                        input_media=p,
                        output_dir=output_dir,
                        whisper_model=whisper_model,
                        language=language,
                        ollama_url=ollama_url,
                        ollama_model=ollama_model,
                        prompt_template=prompt_template
                    )
                    prog.progress(100)
                    st.success(f"Done: {p.name}")
                    st.write(f"- Clean WAV: `{result.clean_wav}`")
                    st.write(f"- Transcript: `{result.transcript_path}`")
                    st.write(f"- Summary: `{result.summary_path}`")

                    st.download_button(
                        label="Download transcript",
                        data=result.transcript_path.read_text(encoding="utf-8"),
                        file_name=result.transcript_path.name
                    )
                    st.download_button(
                        label="Download summary",
                        data=result.summary_path.read_text(encoding="utf-8"),
                        file_name=result.summary_path.name
                    )

                except (FFmpegError, TranscriptionError, OllamaError) as e:
                    log.exception("Pipeline failed")
                    st.error(f"Failed on {p.name}: {e}")
                finally:
                    prog.empty()

    with col2:
        st.subheader("Prompt template")
        st.text_area("Edit prompt (optional)", value=prompt_template, height=260, disabled=True)

if __name__ == "__main__":
    main()
