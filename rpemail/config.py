from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    service_account_file: str = Field(default="credentials/service-account.json")
    admin_email: str = Field(...)

    company_website: str = Field(default="https://returnpolicystays.com")
    logo_url: str = Field(default="https://imgur.com/a/GC86Dxj.png")

    # To update
    template_name: str = Field(default="signature_v1.html")
    users: list[str] = Field(
        default=["nhermann@returnpolicystays.com"],
        description="List of user emails to update signatures for",
    )


settings = Settings()
