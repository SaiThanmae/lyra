"""
Shared config — reads from environment / .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Google Cloud
    google_cloud_project: str = ""
    google_api_key: str = ""
    vertex_ai_location: str = "us-central1"

    # Supabase
    supabase_url: str = ""
    supabase_service_key: str = ""

    # BigQuery
    bigquery_dataset: str = "lyra_corpus"

    # Firebase / Firestore
    firebase_project_id: str = ""


settings = Settings()
