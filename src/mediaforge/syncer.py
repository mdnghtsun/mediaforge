from __future__ import annotations

import logging
import shutil
from pathlib import Path

from mediaforge.config import LibraryConfig
from mediaforge.models import SyncSummary

logger = logging.getLogger(__name__)


class MediaSyncer:
    """Synchronize the staging library to the configured destination."""

    def __init__(self, config: LibraryConfig) -> None:
        self._config = config

    def discover_staged_files(self) -> list[Path]:
        """Return all supported media files found in staging."""
        extensions = {
            f".{extension.lower().lstrip('.')}"
            for extension in self._config.supported_extensions
        }

        staged_files: list[Path] = []

        for path in self._config.staging_directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in extensions:
                staged_files.append(path)

        return sorted(staged_files)

    def sync(self, *, dry_run: bool | None = None) -> SyncSummary:
        """Copy staged files into the configured destination directory."""
        effective_dry_run = (
            self._config.dry_run
            if dry_run is None
            else dry_run
        )

        staging_directory = self._config.staging_directory
        destination_directory = self._config.destination_directory

        if not staging_directory.exists():
            raise FileNotFoundError(
                f"Staging directory does not exist: {staging_directory}"
            )

        if not staging_directory.is_dir():
            raise NotADirectoryError(
                f"Staging path is not a directory: {staging_directory}"
            )

        if not destination_directory.exists():
            raise FileNotFoundError(
                f"Destination directory does not exist or is not mounted: "
                f"{destination_directory}"
            )

        if not destination_directory.is_dir():
            raise NotADirectoryError(
                f"Destination path is not a directory: "
                f"{destination_directory}"
            )

        staged_files = self.discover_staged_files()

        summary = SyncSummary(
            discovered=len(staged_files),
        )

        for source_path in staged_files:
            relative_path = source_path.relative_to(staging_directory)
            destination_path = destination_directory / relative_path

            try:
                if (
                    destination_path.exists()
                    and not self._config.overwrite_existing
                ):
                    logger.info(
                        "Skipping existing destination file: %s",
                        destination_path,
                    )
                    summary.skipped += 1
                    continue

                if effective_dry_run:
                    logger.info(
                        "Would copy: %s -> %s",
                        source_path,
                        destination_path,
                    )
                    summary.copied += 1
                    continue

                destination_path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                shutil.copy(
                    source_path,
                    destination_path,
                )

                logger.info(
                    "Copied: %s -> %s",
                    source_path,
                    destination_path,
                )

                summary.copied += 1

            except Exception:
                logger.exception(
                    "Failed to sync staged file: %s",
                    source_path,
                )
                summary.errors += 1

        return summary