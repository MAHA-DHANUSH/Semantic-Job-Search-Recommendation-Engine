"""
LLM Service — Gemini-powered reasoning & summarization of semantic search results.

Uses the google-genai SDK (google.genai) and auto-discovers the best available
generateContent-capable model for the given API key.
"""

import os
from pathlib import Path

# Load .env from project root (if present) so GEMINI_API_KEY doesn't need
# to be exported manually every shell session.
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass  # python-dotenv is optional; rely on shell env var

from google import genai

_client = None
_chosen_model = None  # cached after first successful discovery

# Preferred model order — first available one wins
_MODEL_PREFERENCE = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.5-flash"
]


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY environment variable is not set.\n"
                "Get a free key at https://aistudio.google.com/app/apikey\n"
                "Then add it to .env:  GEMINI_API_KEY=AIzaSy..."
            )
        # if not api_key.startswith("AIza"):
        #     raise EnvironmentError(
        #         f"GEMINI_API_KEY looks invalid (got: {api_key[:12]}...).\n"
        #         "A valid Gemini API key starts with 'AIzaSy'.\n"
        #         "Get one at https://aistudio.google.com/app/apikey"
        #     )
        _client = genai.Client(api_key=api_key)
    return _client


def _discover_model(client: genai.Client) -> str:
    """
    Ask the API which models are available for this key and return
    the best generateContent-capable one from our preference list.
    Falls back to the first preference if listing fails.
    """
    global _chosen_model
    if _chosen_model:
        return _chosen_model

    try:
        available = {m.name for m in client.models.list()}
        for pref in _MODEL_PREFERENCE:
            # API returns names like "models/gemini-2.0-flash"
            if f"models/{pref}" in available or pref in available:
                _chosen_model = pref
                return pref
    except Exception:
        pass  # If listing fails, fall through to preference list trial

    # Fallback: try each in order during the actual call
    _chosen_model = _MODEL_PREFERENCE[0]
    return _chosen_model


def summarize_results(query: str, results: list) -> str:
    """
    Ask Gemini to reason over the top search results and return
    a concise, human-friendly analysis of which jobs best match the query
    and why.

    Args:
        query:   The user's original free-text search.
        results: List of RealDictRow objects returned by semantic_search().

    Returns:
        A plain-text string with Gemini's reasoning and recommendation.
    """
    if not results:
        return "No results to analyse."

    # Build a compact job snapshot for the LLM context
    jobs_text = ""
    for rank, row in enumerate(results, 1):
        tags = ", ".join(row["tags"]) if row["tags"] else "—"
        pct  = row["similarity"] * 100
        jobs_text += (
            f"\n#{rank}  {row['title']} @ {row['company']}\n"
            f"     Location: {row['location']} | Salary: {row['salary'] or '—'}\n"
            f"     Tags: {tags}\n"
            f"     Similarity score: {pct:.1f}%\n"
        )

    prompt = f"""You are a smart job-search assistant.

A user searched for: "{query}"

Here are the top semantic search results ranked by vector similarity:
{jobs_text}

Tasks:
1. Briefly reason (1-2 sentences per job) about *why* each job matches or doesn't fully match the query.
2. Give a final recommendation: which job(s) are the best fit and what the user should consider next.
3. If none are a great match, say so clearly and suggest how the user could refine their search.

Be concise, direct, and use bullet points. Do NOT repeat the full job list."""

    client = _get_client()
    model_name = _discover_model(client)

    # Try preferred model, then fall through the full list on 404 or quota errors
    tried = set()
    for candidate in [model_name] + _MODEL_PREFERENCE:
        if candidate in tried:
            continue
        tried.add(candidate)
        try:
            response = client.models.generate_content(
                model=candidate,
                contents=prompt,
            )
            global _chosen_model
            _chosen_model = candidate  # remember what worked
            return response.text.strip()
        except Exception as e:
            err = str(e)
            if "404" in err or "NOT_FOUND" in err or "429" in err or "RESOURCE_EXHAUSTED" in err:
                continue  # try next model
            raise  # unexpected error — surface it

    raise RuntimeError(
        "No Gemini model could be reached. Check your API key and quota at "
        "https://aistudio.google.com/app/apikey"
    )
