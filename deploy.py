import requests
from .exceptions import HTTPException


def add_deploy_key(workspace, repository, user, password, public_key, label) -> None:
    response = requests.post(
        url=f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/deploy-keys',
        data={
            'key': public_key,
            'label': label,
        },
        auth=(user, password),
    )

    if response.status_code == 400:
        # Someone has already registered this key as a deploy key for this repository
        pass
    elif not str(response.status_code).startswith("2"):
        raise HTTPException(response)
