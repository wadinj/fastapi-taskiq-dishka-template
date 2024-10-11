from urllib.parse import quote

from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "admin"
    POSTGRES_DB: str = "dishka"
    POSTGRES_ENDPOINT: str = "localhost:15432"

    def get_db_url(user: str, password: str, endpoint: str, db: str) -> str:
        return f"postgresql+psycopg2://{quote(user)}:{quote(password)}@{endpoint}/{db}"


app_settings = AppSettings()
