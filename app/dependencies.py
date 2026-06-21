from fastapi import Header

from .security import verify_token


def get_current_user(
    authorization: str = Header(None)
):

    if not authorization:

        return None

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    return payload