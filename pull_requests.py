from typing import Any, Dict

from requests_oauthlib import OAuth2Session


def get_pr(
    *,
    session: OAuth2Session,
    workspace: str,
    repo_slug: str,
    pull_request_id: int,
) -> Any:
    response = session.get(
        f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}",
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to get PR: {response.content}")
    return response.json()


def update_pr(
    *,
    session: OAuth2Session,
    workspace: str,
    repo_slug: str,
    pull_request_id: int,
    payload: Dict[str, Any],
) -> None:
    response = session.put(
        f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}",
        json=payload,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to modify PR: {response.content}")


def decline_pr(
    *,
    session: OAuth2Session,
    workspace: str,
    repo_slug: str,
    pull_request_id: int,
) -> None:
    response = session.post(
        f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/pullrequests/{pull_request_id}/decline",
    )
    if response.status_code != 200:
        raise RuntimeError(f"Failed to decline PR: {response.content}")
