import difflib

from rpemail.config import settings
from rpemail.google_api import (
    MissingUserInfoError,
    UserInfo,
    get_signature,
    get_user_info,
    update_signature,
)
from rpemail.logging import get_logger
from rpemail.template import render_signature

logger = get_logger("rpemail.main")


def show_signature_diff(email: str, old_html: str, new_html: str) -> bool:
    """Show unified diff between old and new signature. Returns True if changes exist."""
    old_lines = old_html.splitlines(keepends=True)
    new_lines = new_html.splitlines(keepends=True)

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=f"{email} (current)",
            tofile=f"{email} (new)",
        )
    )

    if not diff:
        logger.info("email=%s status=no_changes", email)
        return False

    print("".join(diff))
    return True


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


def main(*, dry_run: bool = False) -> None:
    if not settings.users:
        logger.warning("No users configured")
        return

    users_info = fetch_all_users()

    if dry_run:
        logger.info("Dry run mode - showing diffs")
        for user_info in users_info:
            current_html = get_signature(user_info.email)
            new_html = render_signature(user_info)
            show_signature_diff(user_info.email, current_html, new_html)
    else:
        logger.info("Updating signatures")
        for user_info in users_info:
            html = render_signature(user_info)
            update_signature(user_info.email, html)
            logger.info("email=%s status=updated", user_info.email)

    logger.info("Complete")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Update Gmail signatures")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show diff without updating signatures",
    )
    args = parser.parse_args()
    main(dry_run=args.dry_run)
