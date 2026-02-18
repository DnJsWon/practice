# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # .env 파일에 있는 변수명과 똑같이 써야 합니다.
    DATABASE_URL: str

    class Config:
        env_file = ".env"

# 이 변수를 다른 파일에서 불러다 씁니다.
settings = Settings()