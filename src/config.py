from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8"
    )

    # Postgres Database settings
    pghost: str
    pgport: int
    pguser: str
    pgpassword: str
    pgdb: str

    # OpenAI API
    openai_api_key: str
    openai_base_url: str
    openai_model: str

    # Etc
    number_last_message: int = 3
    host_app: str = "0.0.0.0"
    port_app: int = 8000

    @property
    def pgurl(self) -> str:
        return f"postgresql://{self.pguser}:{self.pgpassword}@{self.pghost}:{self.pgport}/{self.pgdb}"