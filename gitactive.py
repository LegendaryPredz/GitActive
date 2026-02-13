from collections import Counter
from typing import Any, Dict, Optional, Tuple

import requests
import typer
from rich.console import Console
from rich.table import Table

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

    if event_type == "CreateEvent":
        return f"Created a new repo: {repo_name}"
    if event_type == "DeleteEvent":
        delete_type = payload.get("ref_type", "")
        delete_name = payload.get("ref", "")
        if delete_type == "branch":
            return f"Deleted branch: {delete_name}"
        if delete_type == "tag":
            return f"Deleted tag: {delete_name}"
        return f"Deleted {repo_name}"
    if event_type == "ForkEvent":
        forkee = payload.get("forkee", "")
        return f"Forked a repo: {forkee.get('full_name', '')}"
    if event_type == "GollumEvent":
        num_pages_updated = len(payload.get("pages"))
        if num_pages_updated == 1:
            return f"Created/Updated {num_pages_updated} wiki page for: {repo_name}"
        else:
            return f"Created/Updated {num_pages_updated} wiki pages for: {repo_name}"
    if event_type == "IssuesEvent":
        issue_type = payload.get("action", "")
        issue_number = payload.get("issue", "").get("number", "")
        if issue_type == "opened":
            return f"Opened issue {issue_number} in {repo_name}"
        if issue_type == "closed":
            return f"Closed issue {issue_number} in {repo_name}"
        if issue_type == "reopened":
            return f"Reopened issue {issue_number} in {repo_name}"
    if event_type == "PushEvent":
        commits = payload.get("commits")
        if commits:
            return f"Pushed {len(commits)} commit(s) to {repo_name}"
        return f"Pushed to {repo_name}"
    if event_type == "WatchEvent":
        return f"Starred {repo_name}"

    return f"{event_type} in {repo_name}"


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
