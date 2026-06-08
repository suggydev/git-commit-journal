import random
from datetime import datetime

QUOTES = [
    "If debugging is the process of removing software bugs, then programming must be the process of putting them in. — Edsger Dijkstra",
    "A user interface is like a joke. If you have to explain it, it's not that good.",
    "It works on my machine. — Every developer, ever.",
    "First, solve the problem. Then, write the code. — John Johnson",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand. — Martin Fowler",
    "Java is to JavaScript what car is to Carpet. — Chris Heilmann",
    "The only way to go fast, is to go well. — Robert C. Martin",
]

EMOJIS = ["✨", "🚀", "🔥", "🐛", "📝", "🤖", "☕", "🍕", "🦄", "🦀"]


def _get_random_emoji() -> str:
    return random.choice(EMOJIS)


def _get_random_quote() -> str:
    return random.choice(QUOTES)


def _build_stats(commits: list) -> str:
    total_commits = len(commits)
    all_files = set()
    for c in commits:
        all_files.update(c.files)
    total_files = len(all_files)

    lines = [
        "## Stats",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Commits | {total_commits} |",
        f"| Unique files touched | {total_files} |",
        "",
        "<details>",
        "<summary>Files changed</summary>",
        "",
        "\n".join(f"- `{f}`" for f in sorted(all_files)),
        "",
        "</details>",
    ]
    return "\n".join(lines)


def render(journal: str, commits: list, output: str | None) -> None:
    emoji = _get_random_emoji()
    quote = _get_random_quote()
    stats = _build_stats(commits)
    today = datetime.now().strftime("%Y-%m-%d")

    markdown = (
        f"# {emoji} Dev Journal — {today}\n\n"
        f"{journal}\n\n"
        f"{stats}\n\n"
        f"---\n\n"
        f"> {quote}\n"
    )

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(markdown)
    else:
        print(markdown)
