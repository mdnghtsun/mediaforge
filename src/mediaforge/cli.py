from __future__ import annotations

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path

from mediaforge.config import load_config
from mediaforge.organizer import MusicOrganizer


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="mediaforge",
        description="Organize music into a BMW-friendly USB library.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    organize_parser = subparsers.add_parser(
        "organize",
        help="Scan and organize music files.",
    )

    organize_parser.add_argument(
        "--config",
        default="config/library.yaml",
        help="Path to the configuration file.",
    )

    organize_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without modifying files.",
    )

    return parser


def configure_logging(verbose: bool) -> None:
    """Configure application logging."""
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the MediaForge command-line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)

    configure_logging(args.verbose)

    if args.command == "organize":
        config = load_config(Path(args.config))
        effective_dry_run = args.dry_run or config.dry_run

        organizer = MusicOrganizer(config)

        logging.info("MediaForge organizer")
        logging.info("Download directory: %s", config.download_directory)
        logging.info("Staging directory: %s", config.staging_directory)
        logging.info("USB destination: %s", config.destination_directory)
        logging.info("Transfer mode: %s", config.transfer_mode)
        logging.info("Dry run: %s", effective_dry_run)

        summary = organizer.organize(
            dry_run=effective_dry_run,
        )

        action_label = (
            "Would move"
            if effective_dry_run and config.transfer_mode == "move"
            else "Would copy"
            if effective_dry_run
            else "Moved"
            if config.transfer_mode == "move"
            else "Copied"
        )

        logging.info("")
        logging.info("MediaForge complete")
        logging.info("Discovered: %d", summary.discovered)
        logging.info("%s: %d", action_label, summary.transferred)
        logging.info("Skipped: %d", summary.skipped)
        logging.info("Errors: %d", summary.errors)

        return 1 if summary.errors else 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())