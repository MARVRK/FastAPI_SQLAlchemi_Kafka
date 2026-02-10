from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=BASE_DIR / ".env.local",
	                                  env_file_encoding="utf-8",
									  extra = "ignore")
	POSTGRES_DB_PRODUCTS : str
	POSTGRES_USER_PRODUCTS : str
	POSTGRES_PASSWORD_PRODUCTS :str
	PG_CONNECTION_PRODUCTS :str

settings = Settings()
