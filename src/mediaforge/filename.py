from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from .models import TrackMetadata


_INVALID_FILENAME_CHARACTERS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_WHITESPACE = re.compile(r"\s+")
_REPEATED_DASHES = re.compile(r"-{2,}")
_YOUTUBE_ID_SUFFIX = re.compile(r"\s*\[[A-Za-z0-9_-]{11}\]$")


def normalize_text(value: str) -> str:
    """Normalize Unicode and collapse unnecessary whitespace."""
    normalized = unicodedata.normalize("NFKC", value)
    return _WHITESPACE.sub(" ", normalized).strip()


def sanitize_filename_component(value: str) -> str:
    """Return a filesystem-safe artist or title component."""
    sanitized = normalize_text(value)
    sanitized = _INVALID_FILENAME_CHARACTERS.sub("", sanitized)
    sanitized = _REPEATED_DASHES.sub("-", sanitized)
    sanitized = sanitized.strip(" .-_")

    return sanitized or "Unknown"


def build_filename(
    artist: str,
    title: str,
    extension: str,
    filename_format: str = "{artist} - {title}",
) -> str:
    """Build a normalized filename while preserving the extension."""
    clean_artist = sanitize_filename_component(artist)
    clean_title = sanitize_filename_component(title)
    clean_extension = extension.lower().lstrip(".")

    stem = filename_format.format(
        artist=clean_artist,
        title=clean_title,
    )
    stem = sanitize_filename_component(stem)

    if not clean_extension:
        return stem

    return f"{stem}.{clean_extension}"

def strip_youtube_id(value: str) -> str:
    """Remove a trailing YouTube video ID from a filename stem."""
    return _YOUTUBE_ID_SUFFIX.sub("", value).strip()

def parse_filename_metadata(path: Path) -> TrackMetadata:
    """Parse conservative artist/title metadata from a filename."""
    stem = strip_youtube_id(path.stem)

    if " - " in stem:
        artist, title = stem.split(" - ", maxsplit=1)

        return TrackMetadata(
            artist=artist.strip() or None,
            title=title.strip(),
            source_path=path,
        )

    return TrackMetadata(
        artist=None,
        title=stem,
        source_path=path,
    )