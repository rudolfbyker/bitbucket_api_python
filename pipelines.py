from typing import Tuple
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
