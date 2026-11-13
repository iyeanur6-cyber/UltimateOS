"""Detail views for WiFi network list and Bluetooth device list."""

import threading
import logging

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------ #
#  WiFi Detail View                                                    #
# ------------------------------------------------------------------ #
class WiFiDetailView(Gtk.Box):
    """Expandable WiFi view: back button, toggle, network list."""

    def __init__(self, backend, on_back=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._backend = backend
        self._on_back = on_back

        # Header: back button + title + toggle switch
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.get_style_context().add_class("qs-detail-header")

        back_btn = Gtk.Button()
        back_btn.set_relief(Gtk.ReliefStyle.NONE)
        back_img = Gtk.Image.new_from_icon_name("go-previous-symbolic",
                                                 Gtk.IconSize.BUTTON)
        back_btn.set_image(back_img)
        back_btn.get_style_context().add_class("qs-detail-back")
        back_btn.connect("clicked", lambda w: on_back() if on_back else None)
        header.pack_start(back_btn, False, False, 0)

        title = Gtk.Label(label="WiFi")
        title.get_style_context().add_class("qs-detail-title")
        title.set_hexpand(True)
        title.set_xalign(0)
        header.pack_start(title, True, True, 0)

        self._switch = Gtk.Switch()
        self._switch.get_style_context().add_class("qs-switch")
        self._switch.set_valign(Gtk.Align.CENTER)
        self._switch_handler = self._switch.connect("notify::active",
                                                     self._on_switch_toggled)
        header.pack_end(self._switch, False, False, 0)

        self.pack_start(header, False, False, 8)

        # Separator
        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("qs-separator")
        self.pack_start(sep, False, False, 0)

        # Scrollable network list
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        scroll.set_max_content_height(300)

        self._list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._list_box.set_margin_top(4)
        scroll.add(self._list_box)
        self.pack_start(scroll, True, True, 0)

        # Footer: Network Settings
        footer_btn = Gtk.Button(label="Network Settings")
        footer_btn.set_relief(Gtk.ReliefStyle.NONE)
        footer_btn.get_style_context().add_class("qs-settings-btn")
        footer_btn.set_halign(Gtk.Align.START)
        footer_btn.connect("clicked", self._on_settings)
        self.pack_start(footer_btn, False, False, 4)

        # Loading spinner
        self._spinner = Gtk.Spinner()
        self._spinner.set_halign(Gtk.Align.CENTER)

    def refresh(self):
        """Reload WiFi state and network list in background."""
        # Update switch state
        enabled = self._backend.is_enabled()
        self._switch.handler_block(self._switch_handler)
        self._switch.set_active(enabled)
        self._switch.handler_unblock(self._switch_handler)

        # Clear list and show spinner
        for child in self._list_box.get_children():
            self._list_box.remove(child)
        self._list_box.pack_start(self._spinner, False, False, 20)
        self._spinner.start()
        self._list_box.show_all()

        # Fetch networks in background
        threading.Thread(target=self._fetch_networks, daemon=True).start()

    def _fetch_networks(self):
        networks = self._backend.list_networks()
        GLib.idle_add(self._populate_networks, networks)

    def _populate_networks(self, networks):
        self._spinner.stop()
        for child in self._list_box.get_children():
            self._list_box.remove(child)

        if not networks:
            lbl = Gtk.Label(label="No networks found")
            lbl.get_style_context().add_class("qs-row-sublabel")
            lbl.set_margin_top(20)
            self._list_box.pack_start(lbl, False, False, 0)
        else:
            for net in networks:
                row = self._build_network_row(net)
                self._list_box.pack_start(row, False, False, 0)

        self._list_box.show_all()

    def _build_network_row(self, net):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.get_style_context().add_class("qs-network-row")

        # Connected indicator
        if net["in_use"]:
            dot = Gtk.Label(label="\u25CF")
            dot.get_style_context().add_class("qs-connected-dot")
        else:
            dot = Gtk.Label(label="  ")
        row.pack_start(dot, False, False, 0)

        # SSID
        ssid_label = Gtk.Label(label=net["ssid"])
        ssid_label.set_xalign(0)
        ssid_label.set_hexpand(True)
        ssid_label.set_ellipsize(3)
        ssid_label.get_style_context().add_class("qs-row-label")
        row.pack_start(ssid_label, True, True, 0)

        # Security icon
        if net["security"] and net["security"] != "--":
            lock = Gtk.Image.new_from_icon_name("network-wireless-encrypted-symbolic",
                                                 Gtk.IconSize.MENU)
            lock.set_tooltip_text(net["security"])
            row.pack_start(lock, False, False, 0)

        # Signal strength
        sig = net["signal"]
        if sig >= 75:
            sig_icon = "network-wireless-signal-excellent-symbolic"
            sig_class = "qs-signal-strong"
        elif sig >= 50:
            sig_icon = "network-wireless-signal-good-symbolic"
            sig_class = "qs-signal"
        elif sig >= 25:
            sig_icon = "network-wireless-signal-ok-symbolic"
            sig_class = "qs-signal"
        else:
            sig_icon = "network-wireless-signal-weak-symbolic"
            sig_class = "qs-signal"
        sig_img = Gtk.Image.new_from_icon_name(sig_icon, Gtk.IconSize.MENU)
        sig_img.get_style_context().add_class(sig_class)
        row.pack_start(sig_img, False, False, 0)

        # Connect/Disconnect button
        if net["in_use"]:
            btn = Gtk.Button(label="Disconnect")
            btn.connect("clicked", lambda w: self._do_disconnect())
        else:
            btn = Gtk.Button(label="Connect")
            btn.connect("clicked", lambda w, s=net["ssid"]: self._do_connect(s))
        btn.get_style_context().add_class("qs-row-btn")
        row.pack_start(btn, False, False, 0)

        return row

    def _do_connect(self, ssid):
        threading.Thread(target=self._connect_bg, args=(ssid,), daemon=True).start()

    def _connect_bg(self, ssid):
        self._backend.connect(ssid)
        GLib.idle_add(self.refresh)

    def _do_disconnect(self):
        threading.Thread(target=self._disconnect_bg, daemon=True).start()

    def _disconnect_bg(self):
        self._backend.disconnect()
        GLib.idle_add(self.refresh)

    def _on_switch_toggled(self, switch, pspec):
        active = switch.get_active()
        threading.Thread(target=self._toggle_bg, args=(active,), daemon=True).start()

    def _toggle_bg(self, on):
        self._backend.set_enabled(on)
        GLib.idle_add(self.refresh)

    def _on_settings(self, *_):
        import subprocess
        subprocess.Popen(["cinnamon-settings", "network"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


# ------------------------------------------------------------------ #
#  Bluetooth Detail View                                               #
# ------------------------------------------------------------------ #
class BluetoothDetailView(Gtk.Box):
    """Expandable Bluetooth view: back button, toggle, device list."""

    def __init__(self, backend, on_back=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self._backend = backend
        self._on_back = on_back

        # Header
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.get_style_context().add_class("qs-detail-header")

        back_btn = Gtk.Button()
        back_btn.set_relief(Gtk.ReliefStyle.NONE)
        back_img = Gtk.Image.new_from_icon_name("go-previous-symbolic",
                                                 Gtk.IconSize.BUTTON)
        back_btn.set_image(back_img)
        back_btn.get_style_context().add_class("qs-detail-back")
        back_btn.connect("clicked", lambda w: on_back() if on_back else None)
        header.pack_start(back_btn, False, False, 0)

        title = Gtk.Label(label="Bluetooth")
        title.get_style_context().add_class("qs-detail-title")
        title.set_hexpand(True)
        title.set_xalign(0)
        header.pack_start(title, True, True, 0)

        self._switch = Gtk.Switch()
        self._switch.get_style_context().add_class("qs-switch")
        self._switch.set_valign(Gtk.Align.CENTER)
        self._switch_handler = self._switch.connect("notify::active",
                                                     self._on_switch_toggled)
        header.pack_end(self._switch, False, False, 0)

        self.pack_start(header, False, False, 8)

        sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sep.get_style_context().add_class("qs-separator")
        self.pack_start(sep, False, False, 0)

        # Device list
        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scroll.set_min_content_height(200)
        scroll.set_max_content_height(300)

        self._list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self._list_box.set_margin_top(4)
        scroll.add(self._list_box)
        self.pack_start(scroll, True, True, 0)

        # Footer
        footer_btn = Gtk.Button(label="Bluetooth Settings")
        footer_btn.set_relief(Gtk.ReliefStyle.NONE)
        footer_btn.get_style_context().add_class("qs-settings-btn")
        footer_btn.set_halign(Gtk.Align.START)
        footer_btn.connect("clicked", self._on_settings)
        self.pack_start(footer_btn, False, False, 4)

        self._spinner = Gtk.Spinner()
        self._spinner.set_halign(Gtk.Align.CENTER)

    def refresh(self):
        """Reload Bluetooth state and device list."""
        powered = self._backend.is_powered()
        self._switch.handler_block(self._switch_handler)
        self._switch.set_active(powered)
        self._switch.handler_unblock(self._switch_handler)

        for child in self._list_box.get_children():
            self._list_box.remove(child)

        if not powered:
            lbl = Gtk.Label(label="Bluetooth is off")
            lbl.get_style_context().add_class("qs-row-sublabel")
            lbl.set_margin_top(20)
            self._list_box.pack_start(lbl, False, False, 0)
            self._list_box.show_all()
            return

        self._list_box.pack_start(self._spinner, False, False, 20)
        self._spinner.start()
        self._list_box.show_all()

        threading.Thread(target=self._fetch_devices, daemon=True).start()

    def _fetch_devices(self):
        devices = self._backend.get_devices()
        GLib.idle_add(self._populate_devices, devices)

    def _populate_devices(self, devices):
        self._spinner.stop()
        for child in self._list_box.get_children():
            self._list_box.remove(child)

        connected = [d for d in devices if d["connected"]]
        paired = [d for d in devices if not d["connected"]]

        if connected:
            lbl = Gtk.Label(label="Connected")
            lbl.set_xalign(0)
            lbl.get_style_context().add_class("qs-section-label")
            self._list_box.pack_start(lbl, False, False, 0)
            for dev in connected:
                row = self._build_device_row(dev)
                self._list_box.pack_start(row, False, False, 0)

        if paired:
            lbl = Gtk.Label(label="Paired")
            lbl.set_xalign(0)
            lbl.get_style_context().add_class("qs-section-label")
            self._list_box.pack_start(lbl, False, False, 0)
            for dev in paired:
                row = self._build_device_row(dev)
                self._list_box.pack_start(row, False, False, 0)

        if not devices:
            lbl = Gtk.Label(label="No paired devices")
            lbl.get_style_context().add_class("qs-row-sublabel")
            lbl.set_margin_top(20)
            self._list_box.pack_start(lbl, False, False, 0)

        self._list_box.show_all()

    def _build_device_row(self, dev):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        row.get_style_context().add_class("qs-network-row")

        # Connected indicator
        if dev["connected"]:
            dot = Gtk.Label(label="\u25CF")
            dot.get_style_context().add_class("qs-connected-dot")
        else:
            dot = Gtk.Label(label="  ")
        row.pack_start(dot, False, False, 0)

        # Device name
        name_label = Gtk.Label(label=dev["name"])
        name_label.set_xalign(0)
        name_label.set_hexpand(True)
        name_label.set_ellipsize(3)
        name_label.get_style_context().add_class("qs-row-label")
        row.pack_start(name_label, True, True, 0)

        # Battery
        if dev["battery"] is not None:
            bat_label = Gtk.Label(label=f"\U0001F50B {dev['battery']}%")
            bat_label.get_style_context().add_class("qs-row-sublabel")
            row.pack_start(bat_label, False, False, 0)

        # Connect/Disconnect button
        if dev["connected"]:
            btn = Gtk.Button(label="Disconnect")
            btn.connect("clicked",
                        lambda w, m=dev["mac"]: self._do_disconnect(m))
        else:
            btn = Gtk.Button(label="Connect")
            btn.connect("clicked",
                        lambda w, m=dev["mac"]: self._do_connect(m))
        btn.get_style_context().add_class("qs-row-btn")
        row.pack_start(btn, False, False, 0)

        return row

    def _do_connect(self, mac):
        threading.Thread(target=self._connect_bg, args=(mac,), daemon=True).start()

    def _connect_bg(self, mac):
        self._backend.connect_device(mac)
        GLib.idle_add(self.refresh)

    def _do_disconnect(self, mac):
        threading.Thread(target=self._disconnect_bg, args=(mac,), daemon=True).start()

    def _disconnect_bg(self, mac):
        self._backend.disconnect_device(mac)
        GLib.idle_add(self.refresh)

    def _on_switch_toggled(self, switch, pspec):
        active = switch.get_active()
        threading.Thread(target=self._toggle_bg, args=(active,), daemon=True).start()

    def _toggle_bg(self, on):
        self._backend.set_powered(on)
        import time
        time.sleep(1)
        GLib.idle_add(self.refresh)

    def _on_settings(self, *_):
        import subprocess
        subprocess.Popen(["blueman-manager"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
