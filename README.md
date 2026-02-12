# GitActive

A simple command-line tool that shows what a GitHub user has been up to lately. Fetches recent activity from the GitHub Events API and displays it in a clean table — no API key required.

---

## Installation

```bash
pip install git+https://github.com/LegendaryPredz/GitActive.git
```

> Requires **Python 3.13+**

---

## Quick Start

```bash
gitactive kamranahmedse
```

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ kamranahmedse's Events                                     ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Pushed 3 commit(s) to kamranahmedse/developer-roadmap      │
│ Starred kamranahmedse/developer-roadmap (2 times)          │
│ Pushed 1 commit(s) to kamranahmedse/dotfiles               │
└────────────────────────────────────────────────────────────┘
```

---

## Usage

Just pass any GitHub username as an argument:

```bash
gitactive <username>
```

The tool will fetch the user's most recent public events and display them grouped by activity, with repeated events showing a count.

---

## What It Shows

GitActive currently formats the following event types:

| Event | Example Output |
|-------|---------------|
| Push | `Pushed 3 commit(s) to user/repo` |
| Star | `Starred user/repo` |

Duplicate events are grouped together with a count (e.g., `Starred user/repo (2 times)`).

---

## Tips

- **No authentication needed** — the tool uses the public GitHub Events API.
- **Rate limits apply** — GitHub allows 60 unauthenticated requests per hour per IP.
- **Only public activity** is visible — private repo events won't appear.

---

## License

MIT
