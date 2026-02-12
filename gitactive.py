from collections import Counter

import typer
import requests
from rich.console import Console
from rich.table import Table

from typing import Tuple, Dict, Any, Optional

app = typer.Typer()

console = Console()


def get_repo_info(event: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], str]:
    repo = event.get("repo")
    if not isinstance(repo, dict):
        return None, ""
    repo_name = repo.get("name") or ""
    return repo, repo_name


def format_event(event: Dict[str, Any]) -> Optional[str]:
    event_type = event.get("type", "")
    _, repo_name = get_repo_info(event)
    payload = event.get("payload", {})

    if event_type == "CommitCommentEvent":
        pass
    if event_type == "CreateEvent":
        pass
    if event_type == "DeleteEvent":
        pass
    if event_type == "DiscussionEvent":
        pass
    if event_type == "ForkEvent":
        pass
    if event_type == "GollumEvent":
        pass
    if event_type == "IssueCommentEvent":
        pass
    if event_type == "IssueEvent":
        pass
    if event_type == "MemberEvent":
        pass
    if event_type == "PublicEvent":
        pass
    if event_type == "PullRequestEvent":
        pass
    if event_type == "PullRequestReviewEvent":
        pass
    if event_type == "PullRequestReviewCommentEvent":
        pass
    if event_type == "PushEvent":
        commits = payload.get("commits")
        if commits:
            return f"Pushed {len(commits)} commit(s) to {repo_name}"
        return f"Pushed to {repo_name}"
    if event_type == "ReleaseEvent":
        pass
    if event_type == "WatchEvent":
        return f"Starred {repo_name}"


@app.command()
def get_events(username: str):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, timeout=10)
    table = Table(f"{username}'s Events")
    if response.status_code == 200:
        events = response.json()
        event_counts: Counter[str] = Counter()
        for event in events:
            description = format_event(event)
            if description:
                event_counts[description] += 1

        for description, count in event_counts.items():
            if count > 1:
                table.add_row(f"{description} ({count} times)")
            else:
                table.add_row(description)

        console.print(table)
    else:
        typer.echo(f"Error fetching events for {username}: {response.status_code}")


if __name__ == "__main__":
    app()
