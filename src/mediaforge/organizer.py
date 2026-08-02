from __future__ import annotations

import logging
from pathlib import Path

from mediaforge.config import LibraryConfig
from mediaforge.copier import transfer_file
from mediaforge.filename import build_filename
from mediaforge.metadata import read_id3_metadata
from mediaforge.models import OrganizationSummary


logger = logging.getLogger(__name__)


class MusicOrganizer:
    """Discovers and organizes supported music files."""

    def __init__(self, config: LibraryConfig) -> None:
        self._config = config

    def discover_music(self) -> list[Path]:
        """Return all supported music files."""
        extensions = {
            f".{extension.lower().lstrip('.')}"
            for extension in self._config.supported_extensions
        }

        music_files: list[Path] = []

        for path in self._config.download_directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in extensions:
                music_files.append(path)

        return sorted(music_files)

    def organize(self, *, dry_run: bool | None = None) -> OrganizationSummary:
        """Organize all discovered music files into genre-based staging folders."""
        effective_dry_run = (
            self._config.dry_run
            if dry_run is None
            else dry_run
        )

        music_files = self.discover_music()

        summary = OrganizationSummary(
            discovered=len(music_files),
        )

        for source_path in music_files:
            try:
                metadata = read_id3_metadata(source_path)

                if not metadata.is_complete:
                    logger.warning(
                        "Skipping file with incomplete metadata: %s",
                        source_path,
                    )
                    summary.skipped += 1
                    continue

                assert metadata.artist is not None
                assert metadata.title is not None

                destination_filename = build_filename(
                    artist=metadata.artist,
                    title=metadata.title,
                    extension=source_path.suffix,
                    filename_format=self._config.filename_format,
                )

                staging_path = (
                    self._config.staging_directory
                    / destination_filename
                )

                transferred = transfer_file(
                    source=source_path,
                    destination=staging_path,
                    mode=self._config.transfer_mode,
                    dry_run=effective_dry_run,
                    overwrite_existing=self._config.overwrite_existing,
                )

                if not transferred:
                    logger.info(
                        "Skipping existing staging file: %s",
                        staging_path,
                    )
                    summary.skipped += 1
                    continue

                action = (
                    "Would move"
                    if effective_dry_run
                    and self._config.transfer_mode == "move"
                    else "Would copy"
                    if effective_dry_run
                    else "Moved"
                    if self._config.transfer_mode == "move"
                    else "Copied"
                )

                logger.info(
                    "%s: %s -> %s",
                    action,
                    source_path,
                    staging_path,
                )

                summary.transferred += 1

            except Exception:
                logger.exception(
                    "Failed to process music file: %s",
                    source_path,
                )
                summary.errors += 1

        return summary