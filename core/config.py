from __future__ import annotations

import os
from pathlib import Path

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_SECRET_KEY: str = Field(default="TESTE", alias="APP_SECRET_KEY")
    APP_VERSION: str
    DB_ENGINE: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    REDIS_URL: str
    DJANGO_SETTINGS_MODULE: str
    ENVIRONMENT: str

    @computed_field
    @property
    def database(self) -> dict:
        # @property → permite acessar instance.database como se fosse um atributo,
        #   não uma função.
        # @computed_field (do Pydantic v2) → indica que o campo é calculado dinamicamente,
        #    não precisa estar definido diretamente no __init__.

        base_dir = Path(__file__).resolve().parent.parent
        name_value: str | Path

        # Allow sqlite path relative to project root
        name_value = self.DB_NAME
        if str(self.DB_ENGINE).endswith("sqlite3"):
            name_value = base_dir / self.DB_NAME

        return {
            "default": {
                "ENGINE": self.DB_ENGINE,
                "NAME": name_value,
                **({"USER": self.DB_USER} if self.DB_USER else {}),
                **({"PASSWORD": self.DB_PASSWORD} if self.DB_PASSWORD else {}),
                **({"HOST": self.DB_HOST} if self.DB_HOST else {}),
                **({"PORT": str(self.DB_PORT)} if self.DB_PORT else {}),
            }
        }

    @computed_field
    @property
    def caches(self) -> dict:
        return {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": self.REDIS_URL,
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                },
            }
        }

    class Config:
        env_file = ".env.tests" if os.environ.get("DJANGO_ENV") == "test" else ".env"
        env_file_encoding = "utf-8"


settings = Settings()
