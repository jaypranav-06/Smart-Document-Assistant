"""Application configuration and settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI Provider Configuration
    ai_provider: str = "ollama"  # "openai" or "ollama"

    # OpenAI Configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"

    # Ollama Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_embedding_model: str = "nomic-embed-text"

    # Vector Database
    chroma_db_path: str = "./chroma_db"

    # Application
    app_env: str = "development"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:3001"

    # File Upload
    max_file_size_mb: int = 50
    upload_dir: str = "./uploads"
    allowed_file_types: str = "pdf"

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def allowed_file_types_list(self) -> List[str]:
        """Parse allowed file types string into list."""
        return [ft.strip() for ft in self.allowed_file_types.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
