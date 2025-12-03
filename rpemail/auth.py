from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build

from rpemail.config import settings

SCOPES = [
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/admin.directory.user.readonly",
]


def get_credentials(user_email: str) -> service_account.Credentials:
    credentials: service_account.Credentials = (
        service_account.Credentials.from_service_account_file(  # type: ignore[no-untyped-call]
            settings.service_account_file,
            scopes=SCOPES,
            subject=user_email,
        )
    )
    return credentials


def get_gmail_service(user_email: str) -> Any:
    credentials = get_credentials(user_email)
    return build("gmail", "v1", credentials=credentials)


def get_directory_service() -> Any:
    credentials = get_credentials(settings.admin_email)
    return build("admin", "directory_v1", credentials=credentials)
