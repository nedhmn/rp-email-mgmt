from dataclasses import dataclass
from typing import Any

from rpemail.auth import get_directory_service, get_gmail_service


class MissingUserInfoError(Exception):
    pass


@dataclass
class UserInfo:
    email: str
    name: str
    title: str
    phone: str


def get_user_info(email: str) -> UserInfo:
    service = get_directory_service()
    user: dict[str, Any] = service.users().get(userKey=email).execute()

    name: str | None = user.get("name", {}).get("fullName")
    if not name:
        raise MissingUserInfoError(f"{email}: missing name")

    title: str | None = None
    orgs: list[dict[str, Any]] = user.get("organizations", [])
    if orgs:
        title = orgs[0].get("title")
    if not title:
        raise MissingUserInfoError(f"{email}: missing job title")

    phone: str | None = None
    phones: list[dict[str, Any]] = user.get("phones", [])
    for p in phones:
        if p.get("primary"):
            phone = p.get("value")
            break
    if not phone and phones:
        phone = phones[0].get("value")
    if not phone:
        raise MissingUserInfoError(f"{email}: missing phone number")

    return UserInfo(
        email=email,
        name=name,
        title=title,
        phone=phone,
    )


def update_signature(email: str, signature_html: str) -> dict[str, Any]:
    service = get_gmail_service(email)

    send_as: dict[str, Any] = service.users().settings().sendAs().patch(
        userId="me",
        sendAsEmail=email,
        body={"signature": signature_html},
    ).execute()

    return send_as


def get_signature(email: str) -> str:
    service = get_gmail_service(email)

    send_as: dict[str, Any] = service.users().settings().sendAs().get(
        userId="me",
        sendAsEmail=email,
    ).execute()

    result: str = send_as.get("signature", "")
    return result
