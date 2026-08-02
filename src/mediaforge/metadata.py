from __future__ import annotations
from pathlib import Path
from mutagen.easyid3 import EasyID3
from .models import TrackMetadata

def read_id3_metadata(path: Path) -> TrackMetadata:
    """Read embedded ID3 metadata from an MP3."""

    tags = EasyID3(path)

    return TrackMetadata(
        artist=tags.get("artist", [None])[0],
        title=tags.get("title", [None])[0],
        album=tags.get("album", [None])[0],
        year=tags.get("date", [None])[0],
        genre=tags.get("genre", [None])[0],
        source_path=path,
    )


def resolve_library_folder(
    genre: str | None,
    *,
    genre_mapping: dict[str, str],
    library_folders: dict[str, str],
) -> str:
    """Resolve embedded genre metadata into a canonical library folder."""
    normalized_mapping = {
        source_genre.strip().casefold(): category
        for source_genre, category in genre_mapping.items()
    }

    if genre and genre.strip():
        category = normalized_mapping.get(
            genre.strip().casefold(),
            "unsorted",
        )
    else:
        category = "unsorted"

    try:
        return library_folders[category]
    except KeyError as error:
        raise ValueError(
            f"Unknown library category: {category!r}"
        ) from error