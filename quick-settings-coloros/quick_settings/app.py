"""Quick Settings GTK Application."""

import logging

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib

logger = logging.getLogger(__name__)


class QuickSettingsApp:
    """Main application — manages tray icon, panel, and polling."""

    def __init__(self):
        self._poll_id = None

    def run(self):
        """Initialize everything and enter the GTK main loop."""
        # Dark theme
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

        # Apply Catppuccin Mocha CSS
        from .theme import apply_theme
        apply_theme()

        from .backends import Backends
        from .panel import PanelWindow
        from .tray import TrayIcon

        logger.info("Initializing Quick Settings")

        self._backends = Backends()
        self._panel = PanelWindow(self._backends)

        # TrayIcon keeps itself alive via Gtk.StatusIcon
        self._tray = TrayIcon(self._panel, self._backends)

        # Poll for dynamic data every 5 seconds (only while visible)
        self._poll_id = GLib.timeout_add_seconds(5, self._poll)

        logger.info("Quick Settings ready")
        Gtk.main()

    def _poll(self):
        """Periodic refresh of changing data."""
        if self._panel.get_visible():
            self._panel.refresh_dynamic()
        return True  # keep timer alive
