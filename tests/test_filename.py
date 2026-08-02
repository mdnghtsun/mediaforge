from mediaforge.filename import (
    build_filename,
    normalize_text,
    sanitize_filename_component,
)


def test_normalize_text_collapses_whitespace() -> None:
    assert normalize_text("  Daft   Punk  ") == "Daft Punk"


def test_sanitize_filename_component_removes_invalid_characters() -> None:
    assert sanitize_filename_component('AC/DC: "Thunderstruck"?') == "ACDC Thunderstruck"


def test_sanitize_filename_component_returns_unknown_when_empty() -> None:
    assert sanitize_filename_component(':"/?*') == "Unknown"


def test_build_filename() -> None:
    result = build_filename(
        artist="Daft Punk",
        title="Around the World",
        extension=".MP3",
    )

    assert result == "Daft Punk - Around the World.mp3"


def test_build_filename_supports_custom_format() -> None:
    result = build_filename(
        artist="Nusrat Fateh Ali Khan",
        title="Mustt Mustt",
        extension="flac",
        filename_format="{title} — {artist}",
    )

    assert result == "Mustt Mustt — Nusrat Fateh Ali Khan.flac"