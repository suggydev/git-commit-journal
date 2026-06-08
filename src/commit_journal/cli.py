import sys

import click
from rich.console import Console

from .ai_summarizer import summarize
from .git_analyzer import get_commits
from .markdown_renderer import render

TUMBLEWEED = r"""
          .-.
         (   )
          \ /
         _/ \_
        /     \
   ~  /  ~   ~  \  ~
  ~  |  ~   ~   |  ~
  ~  |  ~   ~   |  ~
      \  ~   ~  /
       \_______/
"""

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-haiku-20240307",
    "ollama": "llama3.1",
}


@click.command(
    help="Because writing daily reports is the worst. Let a machine do it. You're welcome."
)
@click.option("--days", default=1, show_default=True, help="Days to look back.")
@click.option(
    "--output", "-o", default=None, help="File to save the report. Prints to stdout if omitted."
)
@click.option(
    "--ai-provider",
    default="openai",
    type=click.Choice(["openai", "anthropic", "ollama"]),
    help="LLM provider to use.",
)
@click.option(
    "--model",
    default=None,
    help="Model override. Defaults to sensible choices per provider.",
)
@click.option(
    "--api-key",
    default=None,
    help="API key. Falls back to env vars.",
)
def main(days: int, output: str | None, ai_provider: str, model: str | None, api_key: str | None) -> None:
    console = Console()

    try:
        commits = get_commits(days)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    if not commits:
        console.print(f"[yellow]{TUMBLEWEED}[/yellow]")
        console.print(
            "Wow. So productive. Much commit. Very empty. "
            "(You did nothing today, you magnificent slacker.)"
        )
        sys.exit(0)

    commit_messages = [c.message for c in commits]
    model = model or DEFAULT_MODELS[ai_provider]

    try:
        journal = summarize(commit_messages, ai_provider, model, api_key)
    except Exception as e:
        console.print(f"[red]AI error:[/red] {e}")
        sys.exit(1)

    render(journal, commits, output)
