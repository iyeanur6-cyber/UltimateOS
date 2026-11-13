"""Quick Settings — entry point."""

import sys
import signal
import argparse
import logging

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib


def main():
    parser = argparse.ArgumentParser(description="Quick Settings Panel")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Allow Ctrl+C to quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    GLib.set_prgname("quick-settings")
    GLib.set_application_name("Quick Settings")

    from .app import QuickSettingsApp
    app = QuickSettingsApp()
    app.run()


if __name__ == "__main__":
    main()
