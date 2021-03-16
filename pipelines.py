from typing import Tuple, Dict
import requests
from Crypto.PublicKey import RSA
from .exceptions import HTTPException


def put_key_if_none_exists(workspace, repository, user, password):
    try:
        public = get_public_key(workspace, repository, user, password)
        print(f"{workspace}/{repository} Key pair already set.")
    except HTTPException as e:
        if e.response.status_code == 404:
            print(f"{workspace}/{repository} Generating new key pair.")
            public, private = generate_key_pair()
            put_key_pair(workspace, repository, user, password, public, private)
        else:
            raise e
    print(public)


def generate_key_pair() -> Tuple[str, str]:
    key = RSA.generate(2048)
    private = key.exportKey('PEM').decode()
    public = key.publickey().exportKey('OpenSSH').decode()
    return public, private


def get_public_key(workspace, repository, user, password) -> str:
    response = requests.get(
        url=f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pipelines_config/ssh/key_pair',
        auth=(user, password),
    )

    if not str(response.status_code).startswith("2"):
        raise HTTPException(response)

    return response.json()['public_key']


def put_key_pair(workspace, repository, user, password, public_key, private_key) -> None:
    response = requests.put(
        url=f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pipelines_config/ssh/key_pair',
        json={
            'type': 'pipeline_ssh_key_pair',
            'public_key': public_key,
            'private_key': private_key,
        },
        auth=(user, password),
    )

    if not str(response.status_code).startswith("2"):
        raise HTTPException(response)


def get_known_hosts(workspace, repository, user, password) -> Dict:
    response = requests.get(
        # Trailing slash is significant for this resource URL.
        url=f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pipelines_config/ssh/known_hosts/',
        auth=(user, password),
    )

    if not str(response.status_code).startswith("2"):
        raise HTTPException(response)

    return response.json()


def post_known_host(workspace, repository, user, password, hostname, key_type, key) -> None:
    # It looks like BitBucket will not respond with 409 for duplicate host names, so to prevent duplicating them, we
    # have to check manually before POSTing.
    for h in get_known_hosts(workspace, repository, user, password)['values']:
        if h['hostname'] == hostname:
            # This hostname is already known. No need to post.
            return

    response = requests.post(
        url=f'https://api.bitbucket.org/2.0/repositories/{workspace}/{repository}/pipelines_config/ssh/known_hosts/',
        json={
            'type': 'pipeline_known_host',
            'hostname': hostname,
            'public_key': {
                'type': 'pipeline_ssh_public_key',
                'key_type': key_type,
                'key': key,
            }
        },
        auth=(user, password),
    )

    if not str(response.status_code).startswith("2"):
        raise HTTPException(response)
