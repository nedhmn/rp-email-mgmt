from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    service_account_file: str = Field(default="credentials/service-account.json")
    admin_email: str = Field(...)

    company_website: str = Field(default="https://returnpolicystays.com")
    logo_url: str = Field(default="https://i.imgur.com/8cFKlCD.png")

    # To update
    template_name: str = Field(default="signature_v1.html")
    users: Annotated[list[str], NoDecode] = Field(
        ..., description="List of user emails to update signatures for"
    )

    @field_validator("users", mode="before")
    @classmethod
    def parse_csv_to_list(cls, emails: str) -> list[str]:
        return list(emails.split(","))


settings = Settings()
