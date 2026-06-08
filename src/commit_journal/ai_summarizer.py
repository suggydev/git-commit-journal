import json
import urllib.request

import anthropic
import openai

from .config import ANTHROPIC_KEY, OLLAMA_BASE_URL, OPENAI_KEY


def _build_prompt(messages: list[str]) -> str:
    bullet_list = "\n".join(f"- {m}" for m in messages)
    return (
        f"Based on these Git commit messages:\n{bullet_list}\n\n"
        "Write a 2-3 sentence daily report in the first person. "
        "Start with 'I worked on...', mention 'I fixed...' if relevant, "
        "and end with 'Tomorrow I will...'. Keep it casual and human."
    )


def _ask_openai(prompt: str, model: str, api_key: str) -> str:
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


def _ask_anthropic(prompt: str, model: str, api_key: str) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()


def _ask_ollama(prompt: str, model: str, base_url: str) -> str:
    req = urllib.request.Request(
        f"{base_url}/api/generate",
        data=json.dumps(
            {"model": model, "prompt": prompt, "stream": False}
        ).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        # TODO: I have no idea why Ollama sometimes returns emojis, but people love them, so I'm keeping this hack
        return data["response"].strip()


def summarize(
    messages: list[str], provider: str, model: str, api_key: str | None
) -> str:
    prompt = _build_prompt(messages)

    if provider == "openai":
        key = api_key or OPENAI_KEY
        if not key:
            raise ValueError("OpenAI API key missing. Set OPENAI_API_KEY or pass --api-key.")
        return _ask_openai(prompt, model, key)

    if provider == "anthropic":
        key = api_key or ANTHROPIC_KEY
        if not key:
            raise ValueError("Anthropic API key missing. Set ANTHROPIC_API_KEY or pass --api-key.")
        return _ask_anthropic(prompt, model, key)

    if provider == "ollama":
        return _ask_ollama(prompt, model, OLLAMA_BASE_URL)

    raise ValueError(f"Unknown provider: {provider}")
