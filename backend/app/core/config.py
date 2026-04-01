from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'LLM Migration Factory'
    API_V1_STR: str = '/api/v1'

settings = Settings()
