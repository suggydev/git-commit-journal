# git-commit-journal

![Demo](./demo.gif)

> Because writing daily reports is the worst. Let a machine do it. You're welcome.

## Install

```bash
pip install git-commit-journal
```

## Setup

Create a `.env` file in your repo root (or anywhere):

```bash
cp .env.example .env
```

| Provider | Env Var | Notes |
| --- | --- | --- |
| OpenAI | `OPENAI_API_KEY` | Get one at [platform.openai.com](https://platform.openai.com) |
| Anthropic | `ANTHROPIC_API_KEY` | Get one at [console.anthropic.com](https://console.anthropic.com) |
| Ollama | `OLLAMA_URL` | Defaults to `http://localhost:11434` |

## Features

| Feature | Description |
| --- | --- |
| 🕵️ Git Analysis | Digs through your commit history for the last N days |
| 🤖 AI Summaries | Turns boring commit messages into a first-person journal |
| 📝 Markdown Reports | Clean, pipeable Markdown with stats and random quotes |
| 🎨 Multiple Providers | OpenAI, Anthropic, or local Ollama |
| 🎭 Easter Eggs | If you did nothing, you get a tumbleweed. |

## Usage

```bash
# Daily report (default: last 1 day)
git-commit-journal

# Last 7 days
git-commit-journal --days 7

# Save to file
git-commit-journal --days 7 -o report.md

# Use Anthropic
git-commit-journal --ai-provider anthropic --model claude-3-sonnet-20240229

# Use local Ollama
git-commit-journal --ai-provider ollama --model llama3.1
```

## Contributing

This project thrives on your weird ideas. Found a bug? The AI is probably hungover. Open an issue.
