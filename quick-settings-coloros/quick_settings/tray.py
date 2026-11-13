"""System tray icon using Gtk.StatusIcon.

Left-click  → toggle Quick Settings popup
Right-click → context menu (Quit)
Scroll      → adjust volume
"""

import warnings
import logging

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk

# GtkStatusIcon is deprecated but works perfectly on X11/Cinnamon
warnings.filterwarnings("ignore", ".*StatusIcon.*")
warnings.filterwarnings("ignore", ".*status_icon.*")

logger = logging.getLogger(__name__)


class TrayIcon:
    """System tray icon for Quick Settings."""

    def __init__(self, panel, backends):
        self._panel = panel
        self._audio = backends.audio

        self._icon = Gtk.StatusIcon()
        self._icon.set_from_icon_name("ayatana-settings")
        self._icon.set_tooltip_text("Quick Settings")
        self._icon.set_visible(True)

        self._icon.connect("activate", self._on_activate)
        self._icon.connect("popup-menu", self._on_popup_menu)
        self._icon.connect("scroll-event", self._on_scroll)

    def _on_activate(self, icon):
        """Left-click: toggle popup visibility."""
        if self._panel.get_visible():
            self._panel.hide()
        else:
            self._panel.position_and_show()

    def _on_popup_menu(self, icon, button, time):
        """Right-click: show context menu."""
        menu = Gtk.Menu()

        quit_item = Gtk.MenuItem(label="Quit Quick Settings")
        quit_item.connect("activate", lambda w: Gtk.main_quit())
        menu.append(quit_item)

        menu.show_all()
        menu.popup(None, None, Gtk.StatusIcon.position_menu, icon, button, time)

    def _on_scroll(self, icon, event):
        """Scroll: adjust volume."""
        vol = self._audio.get_volume()
        if event.direction == Gdk.ScrollDirection.UP:
            self._audio.set_volume(min(150, vol + 5))
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self._audio.set_volume(max(0, vol - 5))
        elif event.direction == Gdk.ScrollDirection.SMOOTH:
            # Handle smooth scrolling (touchpad)
            _, dx, dy = event.get_scroll_deltas()
            if dy < 0:
                self._audio.set_volume(min(150, vol + 5))
            elif dy > 0:
                self._audio.set_volume(max(0, vol - 5))
