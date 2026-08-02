from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml


@dataclass(frozen=True)
class LibraryConfig:
    download_directory: Path
    staging_directory: Path
    destination_directory: Path
    supported_extensions: list[str]
    filename_format: str
    dry_run: bool
    overwrite_existing: bool
    transfer_mode: Literal["copy", "move"]


def load_config(path: Path) -> LibraryConfig:
    """Load and validate the application configuration from a YAML file."""
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    transfer_mode = data.get("transfer_mode", "copy")

    if transfer_mode not in {"copy", "move"}:
        raise ValueError(
            "Invalid transfer_mode. Expected 'copy' or 'move', "
            f"but received {transfer_mode!r}."
        )

    return LibraryConfig(
        download_directory=Path(data["download_directory"]),
        staging_directory=Path(data["staging_directory"]),
        destination_directory=Path(data["destination_directory"]),
        supported_extensions=data["supported_extensions"],
        filename_format=data["filename_format"],
        dry_run=data["dry_run"],
        overwrite_existing=data["overwrite_existing"],
        transfer_mode=transfer_mode,
    )