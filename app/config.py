from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    anthropic_api_key: str
    mcp_server_host: str = "0.0.0.0"
    mcp_server_port: int = 8001
    alert_threshold_cpu: float = 85.0
    alert_threshold_error_rate: float = 5.0

    class Config:
        env_file = ".env"

settings = Settings()