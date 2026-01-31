from __future__ import annotations
import requests

class OllamaError(RuntimeError):
    pass

def summarize(ollama_url: str, model: str, prompt: str, timeout_s: int = 600) -> str:
    """
    Calls Ollama local API: /api/generate
    """
    endpoint = f"{ollama_url.rstrip('/')}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }
    try:
        r = requests.post(endpoint, json=payload, timeout=timeout_s)
        if r.status_code != 200:
            raise OllamaError(f"Ollama HTTP {r.status_code}: {r.text[:500]}")
        data = r.json()
        out = (data.get("response") or "").strip()
        if not out:
            raise OllamaError("Ollama returned empty response.")
        return out
    except requests.RequestException as e:
        raise OllamaError(f"Failed to reach Ollama at {endpoint}. Is Ollama running?") from e
