from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=BASE_DIR / ".env",
	                                  env_file_encoding="utf-8",
									  extra = "ignore")
	POSTGRES_DB_ORDERS : str
	POSTGRES_USER_ORDERS : str
	POSTGRES_PASSWORD_ORDERS :str
	PG_CONNECTION_ORDERS :str

settings = Settings()
