from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from rpemail.config import settings
from rpemail.google_api import UserInfo
from rpemail.utils import format_phone

TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_signature(user: UserInfo) -> str:
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
    template = env.get_template(settings.template_name)

    website = settings.company_website
    website_display = website.replace("https://", "www.").replace("http://", "www.")

    return template.render(
        name=user.name,
        title=user.title,
        email=user.email,
        phone=format_phone(user.phone),
        website=website,
        website_display=website_display,
        logo_url=settings.logo_url,
    )
