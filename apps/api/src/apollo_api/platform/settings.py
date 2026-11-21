"""Apollo settings, read from ``APOLLO_*`` environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from ``APOLLO_*`` environment variables.

    ``state_dir`` is disposable state: both SQLite databases are rebuildable or
    operational. ``library_root`` is the user's library, the source of truth for
    their media, and is never created implicitly.
    """

    model_config = SettingsConfigDict(
        env_prefix="APOLLO_", env_file=".env", extra="ignore"
    )

    state_dir: Path = Path(".apollo")
    library_root: Path = Field(
        default_factory=lambda: Path.home() / "Music" / "Library"
    )
    music_xml_path: Path | None = None
    default_page_size: int = 100
    bind_host: str = "127.0.0.1"
    apple_relocation_verified: bool = False
    job_history_limit: int = 500

    @property
    def config_path(self) -> Path:
        """Generated beets configuration file."""
        return self.state_dir / "config" / "config.yaml"

    @property
    def beets_db_path(self) -> Path:
        """The beets library database."""
        return self.state_dir / "db" / "library.db"

    @property
    def apollo_db_path(self) -> Path:
        """Apollo's own database."""
        return self.state_dir / "db" / "apollo.db"

    @property
    def backups_path(self) -> Path:
        """Database backups."""
        return self.state_dir / "db" / "backups"

    @property
    def logs_path(self) -> Path:
        """Log files."""
        return self.state_dir / "logs"

    @property
    def inbox_path(self) -> Path:
        """Incoming files awaiting import."""
        return self.state_dir / "inbox"

    @property
    def trash_path(self) -> Path:
        """Files removed from the library."""
        return self.state_dir / "trash"

    @property
    def cache_path(self) -> Path:
        """Disposable cache."""
        return self.state_dir / "cache"

    @property
    def work_path(self) -> Path:
        """Scratch space for jobs."""
        return self.state_dir / "work"

    @property
    def reports_path(self) -> Path:
        """Generated reports."""
        return self.state_dir / "reports"


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings, built once."""
    return Settings()
