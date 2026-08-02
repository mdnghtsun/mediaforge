from __future__ import annotations

import shutil
from pathlib import Path
from typing import Literal

TransferMode = Literal["copy", "move"]


def transfer_file(
    source: Path,
    destination: Path,
    mode: TransferMode,
    *,
    dry_run: bool,
    overwrite_existing: bool,
) -> bool:
    """
    Copy or move a music file according to the configured behavior.

    Returns True when the file is transferred, or would be transferred
    during a dry run. Returns False when an existing file is skipped.
    """
    if mode not in {"copy", "move"}:
        raise ValueError(f"Unsupported transfer mode: {mode}")

    if destination.exists() and not overwrite_existing:
        return False

    if dry_run:
        return True

    destination.parent.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        destination.unlink()

    if mode == "copy":
        shutil.copy(source, destination)
    else:
        shutil.move(source, destination)

    return True