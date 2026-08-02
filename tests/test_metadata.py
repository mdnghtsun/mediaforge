from pathlib import Path

from mediaforge.filename import (
    parse_filename_metadata,
    strip_youtube_id,
)

from mediaforge.metadata import resolve_library_folder

def test_strip_youtube_id() -> None:
    result = strip_youtube_id(
        "ZYREE - I Still Feel You (Original Mix) [IH4rLXSc4sE]"
    )

    assert result == "ZYREE - I Still Feel You (Original Mix)"


def test_parse_artist_and_title() -> None:
    result = parse_filename_metadata(
        Path(
            "/Volumes/metube/"
            "ZYREE - I Still Feel You (Original Mix) [IH4rLXSc4sE].mp3"
        )
    )

    assert result.artist == "ZYREE"
    assert result.title == "I Still Feel You (Original Mix)"


def test_parse_filename_without_artist() -> None:
    result = parse_filename_metadata(
        Path("/Volumes/metube/maybe.. maybe.mp3")
    )

    assert result.artist is None
    assert result.title == "maybe.. maybe"


def test_preserves_unicode() -> None:
    result = parse_filename_metadata(
        Path("/Volumes/metube/장영규 - 불안한 잠.mp3")
    )

    assert result.artist == "장영규"
    assert result.title == "불안한 잠"

def test_resolve_library_folder_uses_genre_mapping() -> None:
    result = resolve_library_folder(
        "Rock",
        genre_mapping={
            "Rock": "rock",
        },
        library_folders={
            "rock": "04 Rock",
            "unsorted": "99 Unsorted",
        },
    )

    assert result == "04 Rock"


def test_resolve_library_folder_is_case_insensitive() -> None:
    result = resolve_library_folder(
        "HIP-HOP",
        genre_mapping={
            "Hip-Hop": "hip_hop",
        },
        library_folders={
            "hip_hop": "03 Hip-Hop",
            "unsorted": "99 Unsorted",
        },
    )

    assert result == "03 Hip-Hop"


def test_resolve_library_folder_uses_unsorted_for_unknown_genre() -> None:
    result = resolve_library_folder(
        "Music",
        genre_mapping={},
        library_folders={
            "unsorted": "99 Unsorted",
        },
    )

    assert result == "99 Unsorted"


def test_resolve_library_folder_uses_unsorted_for_missing_genre() -> None:
    result = resolve_library_folder(
        None,
        genre_mapping={},
        library_folders={
            "unsorted": "99 Unsorted",
        },
    )

    assert result == "99 Unsorted"