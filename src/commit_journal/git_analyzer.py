from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from git import InvalidGitRepositoryError, Repo


@dataclass(frozen=True)
class CommitInfo:
    message: str
    date: datetime
    files: list[str]


def get_commits(days: int) -> list[CommitInfo]:
    try:
        repo = Repo(Path.cwd())
    except InvalidGitRepositoryError:
        raise RuntimeError("Not a git repository. Go commit something first.") from None

    since = datetime.now() - timedelta(days=days)
    commits = []

    for commit in repo.iter_commits(since=since.isoformat()):
        files = list(commit.stats.files.keys())
        commits.append(
            CommitInfo(
                message=commit.message.strip(),
                date=commit.committed_datetime,
                files=files,
            )
        )

    return commits
