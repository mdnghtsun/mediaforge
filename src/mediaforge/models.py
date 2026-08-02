from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Track:
    """Represents a music file throughout the organization pipeline."""

    source_path: Path

    artist: str | None
    title: str

    extension: str

    destination_filename: str | None = None
    destination_path: Path | None = None


@dataclass(frozen=True)
class TrackMetadata:
    artist: str | None
    title: str | None
    album: str | None = None
    year: str | None = None
    genre: str | None = None
    source_path: Path | None = None

    @property
    def is_complete(self) -> bool:
        """Return whether the required artist and title fields are present."""
        return bool(self.artist and self.title)


@dataclass
class OrganizationSummary:
    """Summary of an organize operation."""

    discovered: int = 0
    transferred: int = 0
    skipped: int = 0
    errors: int = 0

@dataclass
class SyncSummary:
    """Summary of a staging-to-destination sync operation."""

    discovered: int = 0
    copied: int = 0
    skipped: int = 0
    errors: int = 0