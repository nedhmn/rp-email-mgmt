from rpemail.config import settings
from rpemail.google_api import (
    MissingUserInfoError,
    UserInfo,
    get_user_info,
    update_signature,
)
from rpemail.logging import get_logger
from rpemail.template import render_signature

logger = get_logger("rpemail.main")


def fetch_all_users() -> list[UserInfo]:
    users_info = []
    errors = []

    logger.info("Fetching user info")
    for email in settings.users:
        try:
            user_info = get_user_info(email)
            users_info.append(user_info)
            logger.info("email=%s status=ok", email)
        except MissingUserInfoError as e:
            errors.append(str(e))
            logger.error("email=%s status=missing_data", email)

    if errors:
        for error in errors:
            logger.error("error=%s", error)
        raise SystemExit(1)

    return users_info


def main() -> None:
    if not settings.users:
        logger.warning("No users configured")
        return

    users_info = fetch_all_users()

    logger.info("Updating signatures")
    for user_info in users_info:
        html = render_signature(user_info)
        update_signature(user_info.email, html)
        logger.info("email=%s status=updated", user_info.email)

    logger.info("Complete")


if __name__ == "__main__":
    main()
