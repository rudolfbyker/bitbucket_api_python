from requests_oauthlib import OAuth2Session


def delete_branch(
    *,
    session: OAuth2Session,
    workspace: str,
    repo_slug: str,
    branch_name: str,
) -> None:
    response = session.delete(
        f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo_slug}/refs/branches/{branch_name}",
    )
    if response.status_code != 204:
        raise RuntimeError(f"Failed to delete branch: {response.content}")
