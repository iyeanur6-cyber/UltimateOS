"""ColorOS-inspired Quick Settings panel for Cinnamon/GTK3."""
import logging
import threading
import subprocess
from datetime import datetime

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gtk, Gdk, GLib, Pango

from .widgets import ToggleTile, SliderWidget, MediaWidget, BatteryBar
from .detail_view import WiFiDetailView, BluetoothDetailView

logger = logging.getLogger(__name__)


class PanelWindow(Gtk.Window):
    """Borderless, bottom-right quick-settings popup."""

    WIDTH = 470
    HEIGHT = 760

    def __init__(self, backends):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        self.set_app_paintable(True)
        self._backends = backends
        self.set_name("qs-window")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(self.WIDTH, self.HEIGHT)
        self.set_type_hint(Gdk.WindowTypeHint.POPUP_MENU)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_focus_on_map(True)
        self.get_style_context().add_class("qs-window")
        self.connect("focus-out-event", self._on_focus_out)
        self.connect("key-press-event", self._on_key_press)
        self.connect("delete-event", lambda *_: self.hide() or True)

        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self._stack.set_transition_duration(180)
        self.add(self._stack)

        self._build_main()
        self._build_details()
        self.hide()

    # ------------------------------------------------------------------
    # Main UI
    # ------------------------------------------------------------------
    def _build_main(self):
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.get_style_context().add_class("qs-panel")
        root.set_margin_top(10)
        root.set_margin_bottom(10)
        root.set_margin_start(10)
        root.set_margin_end(10)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.set_margin_start(10); header.set_margin_end(10)
        header.set_margin_top(6); header.set_margin_bottom(4)

        self._time = Gtk.Label()
        self._time.set_xalign(0)
        self._time.get_style_context().add_class("qs-time")
        header.pack_start(self._time, True, True, 0)

        self._date = Gtk.Label()
        self._date.get_style_context().add_class("qs-date")
        header.pack_start(self._date, False, False, 8)

        for icon, tooltip, cb in [
            ("document-edit-symbolic", "Edit quick settings", self._edit),
            ("preferences-system-symbolic", "Cinnamon Settings", self._open_settings),
            ("view-more-symbolic", "More", self._show_more),
        ]:
            b = Gtk.Button()
            b.set_relief(Gtk.ReliefStyle.NONE)
            b.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))
            b.set_tooltip_text(tooltip)
            b.get_style_context().add_class("qs-header-btn")
            b.connect("clicked", lambda _w, f=cb: f())
            header.pack_start(b, False, False, 0)
        root.pack_start(header, False, False, 0)

        self._battery = BatteryBar()
        self._battery.get_style_context().add_class("qs-battery-card")
        root.pack_start(self._battery, False, False, 4)

        self._grid = Gtk.Grid()
        self._grid.set_row_spacing(8)
        self._grid.set_column_spacing(8)
        self._grid.set_margin_start(8); self._grid.set_margin_end(8)
        self._grid.set_margin_top(8); self._grid.set_margin_bottom(8)
        self._grid.set_column_homogeneous(True)
        self._grid.set_row_homogeneous(False)
        root.pack_start(self._grid, False, False, 0)

        self.tiles = {}
        # Wi-Fi and Bluetooth remain the two large cards at the top.
        self._add_tile("wifi", "Wi-Fi", "network-wireless-symbolic", 0, 0, self._toggle_wifi, True, self._wifi_detail, 2)
        self._add_tile("bluetooth", "Bluetooth", "bluetooth-active-symbolic", 2, 0, self._toggle_bluetooth, True, self._bluetooth_detail, 2)
        # Compact circular controls below.
        compact = [
            ("airplane", "Airplane", "airplane-mode-symbolic", self._toggle_airplane),
            ("night", "Night Light", "weather-clear-night-symbolic", self._toggle_night),
            ("dnd", "Do Not Disturb", "notifications-disabled-symbolic", self._toggle_dnd),
            ("power", "Power saver", "battery-good-symbolic", self._toggle_power),
            ("hotspot", "Hotspot", "network-wireless-hotspot-symbolic", self._toggle_hotspot),
            ("dark", "Dark mode", "weather-clear-night-symbolic", self._toggle_dark),
            ("mic", "Mute Mic", "microphone-sensitivity-muted-symbolic", self._toggle_mic),
            ("camera", "Camera", "camera-photo-symbolic", self._open_camera),
        ]
        for idx, (key, label, icon, cb) in enumerate(compact):
            col = idx % 4; row = 1 + idx // 4
            self._add_tile(key, label, icon, col, row, cb)

        # Media card spans two columns.
        self._media = MediaWidget(
            on_play_pause=self._backends.media.play_pause,
            on_next=self._backends.media.next,
            on_prev=self._backends.media.previous,
        )
        self._grid.attach(self._media, 0, 3, 4, 1)

        # Sliders in ColorOS-like large cards.
        self._brightness = SliderWidget(
            "display-brightness-symbolic", 0, 100, 1,
            on_changed=lambda v: self._backends.brightness.set_percentage(v),
        )
        self._brightness.get_style_context().add_class("qs-large-slider")
        self._grid.attach(self._brightness, 0, 4, 4, 1)

        self._volume = SliderWidget(
            "audio-volume-high-symbolic", 0, 150, 1,
            on_changed=lambda v: self._backends.audio.set_volume(v),
            on_icon_click=self._backends.audio.toggle_mute,
        )
        self._volume.get_style_context().add_class("qs-large-slider")
        self._grid.attach(self._volume, 0, 5, 4, 1)

        actions = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        actions.set_margin_start(8); actions.set_margin_end(8); actions.set_margin_top(6)
        for icon, label, cb in [
            ("system-lock-screen-symbolic", "Lock", self._lock),
            ("preferences-system-symbolic", "Settings", self._open_settings),
        ]:
            b = Gtk.Button()
            b.set_relief(Gtk.ReliefStyle.NONE)
            b.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON))
            b.set_label(label)
            b.get_style_context().add_class("qs-action-btn")
            b.connect("clicked", lambda _w, f=cb: f())
            actions.pack_start(b, True, True, 0)
        root.pack_start(actions, False, False, 2)

        pages = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        pages.set_halign(Gtk.Align.CENTER)
        for i in range(3):
            dot = Gtk.Label(label="●" if i == 0 else "•")
            dot.get_style_context().add_class("qs-page-dot-active" if i == 0 else "qs-page-dot")
            pages.pack_start(dot, False, False, 0)
        root.pack_end(pages, False, False, 5)

        self._stack.add_named(root, "main")

    def _add_tile(self, key, label, icon, col, row, callback, chevron=False, detail=None, width=1):
        tile = ToggleTile(key, label, icon, has_chevron=chevron,
                          on_toggle=lambda _t: callback(),
                          on_chevron=detail)
        tile.set_hexpand(True)
        tile.set_vexpand(False)
        self.tiles[key] = tile
        self._grid.attach(tile, col, row, width, 1)

    # ------------------------------------------------------------------
    # Detail pages
    # ------------------------------------------------------------------
    def _build_details(self):
        wifi = WiFiDetailView(self._backends.wifi, on_back=self._main_view)
        bt = BluetoothDetailView(self._backends.bluetooth, on_back=self._main_view)
        self._wifi_view = wifi
        self._bt_view = bt
        self._stack.add_named(wifi, "wifi")
        self._stack.add_named(bt, "bluetooth")

    def _wifi_detail(self):
        self._wifi_view.refresh()
        self._stack.set_visible_child_name("wifi")

    def _bluetooth_detail(self):
        self._bt_view.refresh()
        self._stack.set_visible_child_name("bluetooth")

    def _main_view(self):
        self._stack.set_visible_child_name("main")
        self.refresh_dynamic()

    # ------------------------------------------------------------------
    # Backend actions
    # ------------------------------------------------------------------
    def _toggle_wifi(self):
        self._backends.wifi.set_enabled(not self._backends.wifi.is_enabled()); self.refresh_dynamic()

    def _toggle_bluetooth(self):
        self._backends.bluetooth.set_powered(not self._backends.bluetooth.is_powered()); self.refresh_dynamic()

    def _toggle_airplane(self):
        self._backends.airplane.toggle(); self.refresh_dynamic()

    def _toggle_night(self):
        if self._backends.night_light.is_active(): self._backends.night_light.disable()
        else: self._backends.night_light.enable()
        self.refresh_dynamic()

    def _toggle_dnd(self):
        self._backends.dnd.toggle(); self.refresh_dynamic()

    def _toggle_power(self):
        self._backends.power_saver.toggle(); self.refresh_dynamic()

    def _toggle_hotspot(self):
        threading.Thread(target=self._hotspot_bg, daemon=True).start()

    def _hotspot_bg(self):
        self._backends.hotspot.toggle(); GLib.idle_add(self.refresh_dynamic)

    def _toggle_mic(self):
        self._backends.mic.toggle(); self.refresh_dynamic()

    def _open_camera(self):
        if not self._backends.camera.open():
            subprocess.Popen(["cinnamon-settings", "privacy"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.hide()

    def _toggle_dark(self):
        try:
            out = subprocess.check_output(["gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"], text=True).strip()
            dark = "dark" in out.lower()
            subprocess.run(["gsettings", "set", "org.cinnamon.desktop.interface", "gtk-theme", "Mint-Y-Dark" if not dark else "Mint-Y"], check=False)
        except Exception as e:
            logger.debug("dark mode toggle failed: %s", e)
        self.refresh_dynamic()

    def _lock(self):
        subprocess.Popen(["cinnamon-screensaver-command", "--lock"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.hide()

    def _open_settings(self):
        subprocess.Popen(["cinnamon-settings"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _edit(self):
        self._open_settings()

    def _show_more(self):
        # Keep this intentionally lightweight: the second/third page can be added later.
        self._open_settings()

    # ------------------------------------------------------------------
    # State refresh
    # ------------------------------------------------------------------
    def refresh_dynamic(self):
        try:
            wifi_on = self._backends.wifi.is_enabled()
            ssid = self._backends.wifi.get_connected_ssid() if wifi_on else None
            self.tiles["wifi"].set_active(wifi_on, ssid or "On" if wifi_on else "Off")

            bt_on = self._backends.bluetooth.is_powered()
            self.tiles["bluetooth"].set_active(bt_on, "On" if bt_on else "Off")

            self.tiles["airplane"].set_active(self._backends.airplane.active, "On" if self._backends.airplane.active else "Off")
            self.tiles["night"].set_active(self._backends.night_light.is_active(), "On" if self._backends.night_light.is_active() else "Off")
            self.tiles["dnd"].set_active(self._backends.dnd.active, "On" if self._backends.dnd.active else "Off")
            self.tiles["power"].set_active(self._backends.power_saver.is_active(), "On" if self._backends.power_saver.is_active() else "Off")
            self.tiles["hotspot"].set_active(self._backends.hotspot.is_active(), "On" if self._backends.hotspot.is_active() else "Off")

            theme = subprocess.check_output(["gsettings", "get", "org.cinnamon.desktop.interface", "gtk-theme"], text=True).strip()
            dark = "dark" in theme.lower()
            self.tiles["dark"].set_active(dark, "On" if dark else "Off")
            mic_muted = self._backends.mic.is_muted()
            self.tiles["mic"].set_active(mic_muted, "Muted" if mic_muted else "Off")
            self.tiles["camera"].set_active(False, "Open")
        except Exception as e:
            logger.debug("state refresh failed: %s", e)

        try:
            self._brightness.set_value(self._backends.brightness.get_percentage())
        except Exception:
            pass
        try:
            self._volume.set_value(self._backends.audio.get_volume())
        except Exception:
            pass
        try:
            self._media.update(self._backends.media.get_status())
        except Exception:
            pass
        try:
            self._battery.update(self._backends.battery.get_info())
        except Exception:
            pass
        self._update_clock()
        return False

    def _update_clock(self):
        now = datetime.now()
        self._time.set_text(now.strftime("%H:%M"))
        self._date.set_text(now.strftime("%a %d %b"))

    # ------------------------------------------------------------------
    # Popup behavior
    # ------------------------------------------------------------------
    def position_and_show(self):
        self._stack.set_visible_child_name("main")
        self.refresh_dynamic()
        self.show_all()
        self.present()
        self._position_bottom_right()

    def _position_bottom_right(self):
        display = Gdk.Display.get_default()
        monitor = display.get_primary_monitor() if display else None
        if monitor is None and display:
            monitor = display.get_monitor(0)
        if monitor:
            geo = monitor.get_workarea()
            self.move(geo.x + geo.width - self.WIDTH - 14,
                      geo.y + geo.height - self.HEIGHT - 14)

    def _on_focus_out(self, *_):
        # Do not hide immediately when focus moves to a child/detail interaction.
        GLib.timeout_add(100, self._hide_if_unfocused)
        return False

    def _hide_if_unfocused(self):
        if self.get_visible() and not self.is_active():
            self.hide()
        return False

    def _on_key_press(self, _widget, event):
        if event.keyval == Gdk.KEY_Escape:
            self.hide()
            return True
        return False
