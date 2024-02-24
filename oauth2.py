from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


def oauth2__client_credentials__get_session(
    *,
    client_id: str,
    client_secret: str,
) -> OAuth2Session:
    """
    Get an OAuth2 session with access token using the client credentials flow.

    The client credentials flow is appropriate when the client is "private". E.g., a script on your PC or some backend
    service. I.e., where the user can't look inside the app to find the `client_secret`.

    Get a `key` and `secret` from Bitbucket Cloud by creating a new OAuth consumer
    at https://bitbucket.org/{workspace}/workspace/settings/api .

    Examples:
        >>> s = oauth2__client_credentials__get_session(client_id="foo", client_secret="bar")  # doctest: +SKIP
        >>> s.post("https://api.bitbucket.org/2.0/...", json={"some": "thing"})  # doctest: +SKIP

    Args:
        client_id: The "key" from Bitbucket Cloud.
        client_secret: The "Secret" from Bitbucket Cloud.

    Returns:
        The OAuth2 session, with an access token already inside.
    """
    session = OAuth2Session(client=BackendApplicationClient(client_id=client_id))
    session.fetch_token(
        token_url="https://bitbucket.org/site/oauth2/access_token",
        client_id=client_id,
        client_secret=client_secret,
    )
    return session
