from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = 'LLM Migration Factory'
    API_V1_STR: str = '/api/v1'
    
    # AWS Settings
    AWS_REGION: str = 'us-east-1'
    AWS_PROFILE: str | None = None
    
    class Config:
        env_file = ".env"

settings = Settings()
