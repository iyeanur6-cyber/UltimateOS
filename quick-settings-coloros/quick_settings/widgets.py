"""ColorOS-inspired GTK widgets for Quick Settings."""
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango


class ToggleTile(Gtk.Box):
    """Large Wi-Fi/Bluetooth cards or small circular quick toggles."""

    ACCENTS = {
        "wifi": "qs-accent-blue", "bluetooth": "qs-accent-cyan",
        "airplane": "qs-accent-purple", "night": "qs-accent-yellow",
        "dnd": "qs-accent-red", "power": "qs-accent-green",
        "hotspot": "qs-accent-cyan", "dark": "qs-accent-purple",
    }

    def __init__(self, tile_id, label, icon_name, has_chevron=False, on_toggle=None, on_chevron=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.tile_id = tile_id
        self._active = False
        self._wide = tile_id in ("wifi", "bluetooth")
        self._on_toggle = on_toggle

        self._main_btn = Gtk.Button()
        self._main_btn.set_relief(Gtk.ReliefStyle.NONE)
        self._main_btn.set_hexpand(True)
        self._main_btn.connect("clicked", lambda _w: on_toggle(self) if on_toggle else None)

        if self._wide:
            self._build_wide(icon_name, label)
        else:
            self._build_round(icon_name, label)

        self.pack_start(self._main_btn, True, True, 0)

        if has_chevron:
            self._chevron = Gtk.Button()
            self._chevron.set_relief(Gtk.ReliefStyle.NONE)
            self._chevron.set_image(Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.MENU))
            self._chevron.get_style_context().add_class("qs-chevron")
            self._chevron.connect("clicked", lambda _w: on_chevron() if on_chevron else None)
            self.pack_start(self._chevron, False, False, 0)

    def _build_wide(self, icon_name, label):
        self._main_btn.get_style_context().add_class("qs-wide-tile")
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        box.set_margin_start(12); box.set_margin_end(12)
        box.set_margin_top(8); box.set_margin_bottom(8)
        self._circle = Gtk.Box(); self._circle.set_size_request(46, 46)
        self._circle.set_halign(Gtk.Align.CENTER); self._circle.set_valign(Gtk.Align.CENTER)
        self._circle.get_style_context().add_class("qs-wide-circle")
        self._icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
        self._icon.get_style_context().add_class("qs-wide-icon")
        self._circle.add(self._icon); box.pack_start(self._circle, False, False, 0)
        text = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); text.set_valign(Gtk.Align.CENTER)
        self._label = Gtk.Label(label=label); self._label.set_xalign(0); self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._label.get_style_context().add_class("qs-wide-label")
        self._status = Gtk.Label(label="Off"); self._status.set_xalign(0); self._status.get_style_context().add_class("qs-wide-status")
        text.pack_start(self._label, False, False, 0); text.pack_start(self._status, False, False, 0)
        box.pack_start(text, True, True, 0); self._main_btn.add(box)

    def _build_round(self, icon_name, label):
        holder = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        holder.set_halign(Gtk.Align.CENTER); holder.set_valign(Gtk.Align.CENTER)
        self._main_btn.get_style_context().add_class("qs-round-tile")
        self._main_btn.set_size_request(82, 82)
        self._icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.DND)
        self._icon.get_style_context().add_class("qs-round-icon")
        holder.pack_start(self._icon, False, False, 0)
        self._label = Gtk.Label(label=label); self._label.set_xalign(0.5); self._label.set_ellipsize(Pango.EllipsizeMode.END)
        self._label.set_max_width_chars(12); self._label.get_style_context().add_class("qs-round-label")
        holder.pack_start(self._label, False, False, 0)
        self._status = Gtk.Label(label="Off"); self._status.get_style_context().add_class("qs-round-status")
        holder.pack_start(self._status, False, False, 0)
        self._main_btn.add(holder)

    def set_active(self, active, status_text=None):
        self._active = bool(active)
        accent = self.ACCENTS.get(self.tile_id)
        b = self._main_btn.get_style_context()
        i = self._icon.get_style_context()
        s = self._status.get_style_context()
        b.remove_class("qs-wide-tile"); b.remove_class("qs-wide-tile-active")
        b.remove_class("qs-round-tile"); b.remove_class("qs-round-tile-active")
        if accent: b.remove_class(accent)
        if self._wide:
            c = self._circle.get_style_context(); l = self._label.get_style_context()
            c.remove_class("qs-wide-circle"); c.remove_class("qs-wide-circle-active")
            i.remove_class("qs-wide-icon"); i.remove_class("qs-wide-icon-active")
            l.remove_class("qs-wide-label"); l.remove_class("qs-wide-label-active")
            s.remove_class("qs-wide-status"); s.remove_class("qs-wide-status-active")
            if active:
                b.add_class("qs-wide-tile-active"); c.add_class("qs-wide-circle-active"); i.add_class("qs-wide-icon-active"); l.add_class("qs-wide-label-active"); s.add_class("qs-wide-status-active")
                status_text = status_text or "On"
            else:
                b.add_class("qs-wide-tile"); c.add_class("qs-wide-circle"); i.add_class("qs-wide-icon"); l.add_class("qs-wide-label"); s.add_class("qs-wide-status")
                status_text = status_text or "Off"
        else:
            l = self._label.get_style_context()
            i.remove_class("qs-round-icon"); i.remove_class("qs-round-icon-active")
            l.remove_class("qs-round-label"); l.remove_class("qs-round-label-active")
            s.remove_class("qs-round-status"); s.remove_class("qs-round-status-active")
            if active:
                b.add_class("qs-round-tile-active"); i.add_class("qs-round-icon-active"); l.add_class("qs-round-label-active"); s.add_class("qs-round-status-active")
                status_text = status_text or "On"
            else:
                b.add_class("qs-round-tile"); i.add_class("qs-round-icon"); l.add_class("qs-round-label"); s.add_class("qs-round-status")
                status_text = status_text or "Off"
            if active and accent:
                # Keep active state clean; accent is represented by the status indicator.
                pass
        self._status.set_text(status_text)

    @property
    def active(self):
        return self._active


class SliderWidget(Gtk.Box):
    def __init__(self, icon_name, min_val=0, max_val=100, step=5, on_changed=None, on_icon_click=None):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.get_style_context().add_class("qs-slider-box")
        self._on_changed = on_changed; self._programmatic = False
        self._icon_btn = Gtk.Button(); self._icon_btn.set_relief(Gtk.ReliefStyle.NONE)
        self._icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON); self._icon_btn.set_image(self._icon)
        self._icon_btn.get_style_context().add_class("qs-slider-icon")
        if on_icon_click: self._icon_btn.connect("clicked", lambda _w: on_icon_click())
        self.pack_start(self._icon_btn, False, False, 0)
        self._scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, min_val, max_val, step)
        self._scale.set_draw_value(False); self._scale.set_hexpand(True); self._scale.get_style_context().add_class("qs-slider")
        self._scale.connect("value-changed", self._on_value_changed); self.pack_start(self._scale, True, True, 0)
        self._value_label = Gtk.Label(label="0%"); self._value_label.get_style_context().add_class("qs-slider-label"); self.pack_start(self._value_label, False, False, 0)

    def set_value(self, val):
        self._programmatic = True; self._scale.set_value(val); self._value_label.set_text(f"{int(val)}%"); self._programmatic = False
    def get_value(self): return self._scale.get_value()
    def set_icon(self, icon_name): self._icon.set_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
    def _on_value_changed(self, scale):
        val = scale.get_value(); self._value_label.set_text(f"{int(val)}%")
        if not self._programmatic and self._on_changed: self._on_changed(val)


class MediaWidget(Gtk.Box):
    def __init__(self, on_play_pause=None, on_next=None, on_prev=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8); self.get_style_context().add_class("qs-media")
        top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        note = Gtk.Box(); note.set_size_request(52, 52); note.get_style_context().add_class("qs-album"); note.add(Gtk.Image.new_from_icon_name("audio-x-generic-symbolic", Gtk.IconSize.DND)); top.pack_start(note, False, False, 0)
        info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2); info.set_valign(Gtk.Align.CENTER)
        self._title_label = Gtk.Label(label="Not playing"); self._title_label.set_xalign(0); self._title_label.get_style_context().add_class("qs-media-title")
        self._artist_label = Gtk.Label(label=""); self._artist_label.set_xalign(0); self._artist_label.get_style_context().add_class("qs-media-artist")
        info.pack_start(self._title_label, False, False, 0); info.pack_start(self._artist_label, False, False, 0); top.pack_start(info, True, True, 0); self.pack_start(top, False, False, 0)
        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12); controls.set_halign(Gtk.Align.CENTER)
        self._prev_btn = self._make_btn("media-skip-backward-symbolic", on_prev, "qs-media-btn"); self._play_btn = self._make_btn("media-playback-start-symbolic", on_play_pause, "qs-media-btn-play"); self._next_btn = self._make_btn("media-skip-forward-symbolic", on_next, "qs-media-btn")
        for b in (self._prev_btn, self._play_btn, self._next_btn): controls.pack_start(b, False, False, 0)
        self.pack_start(controls, False, False, 0)

    def _make_btn(self, icon, cb, css):
        b = Gtk.Button(); b.set_relief(Gtk.ReliefStyle.NONE); b.set_image(Gtk.Image.new_from_icon_name(icon, Gtk.IconSize.BUTTON)); b.get_style_context().add_class(css)
        if cb: b.connect("clicked", lambda _w: cb())
        return b
    def update(self, info):
        if not info: self._title_label.set_text("Not playing"); self._artist_label.set_text(""); self._set_play_icon(False); return
        self._title_label.set_text(info.get("title") or "Not playing"); artist = info.get("artist") or ""; player = info.get("player") or ""; self._artist_label.set_text(f"{artist}  •  {player}" if artist else player); self._set_play_icon(info.get("status") == "Playing")
    def _set_play_icon(self, playing): self._play_btn.get_image().set_from_icon_name("media-playback-pause-symbolic" if playing else "media-playback-start-symbolic", Gtk.IconSize.BUTTON)


class BatteryBar(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        self._icon = Gtk.Image.new_from_icon_name("battery-full-symbolic", Gtk.IconSize.BUTTON); self._icon.get_style_context().add_class("qs-battery-icon"); self.pack_start(self._icon, False, False, 0)
        self._label = Gtk.Label(label="Battery: --"); self._label.set_xalign(0); self._label.set_hexpand(True); self.pack_start(self._label, True, True, 0)
    def update(self, info):
        if not info: self._label.set_text("No battery"); return
        pct, state = info["percentage"], info["state"]
        icon = "battery-good-charging-symbolic" if state == "Charging" else ("battery-full-symbolic" if pct > 80 else "battery-good-symbolic" if pct > 50 else "battery-low-symbolic" if pct > 20 else "battery-caution-symbolic")
        self._icon.set_from_icon_name(icon, Gtk.IconSize.BUTTON); self._label.set_text(f"{pct:.0f}%  •  {state}")
