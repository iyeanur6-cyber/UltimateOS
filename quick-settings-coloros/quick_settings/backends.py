"""System backends for Quick Settings.

Each backend wraps a system service (NetworkManager, BlueZ, PipeWire, etc.)
using subprocess calls or GObject introspection.
"""

import logging
import os
import re
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


def _run(*args, timeout=3):
    """Run a command and return stdout, or empty string on error."""
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        logger.debug("Command %s failed: %s", args, e)
        return ""


# ------------------------------------------------------------------ #
#  WiFi (NetworkManager / nmcli)                                      #
# ------------------------------------------------------------------ #
class WiFiBackend:
    def is_enabled(self):
        return _run("nmcli", "radio", "wifi") == "enabled"

    def set_enabled(self, on):
        _run("nmcli", "radio", "wifi", "on" if on else "off")

    def get_connected_ssid(self):
        out = _run("nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active")
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) >= 2 and "wireless" in parts[-1]:
                return parts[0]
        return None

    def list_networks(self):
        """Return list of dicts: {ssid, signal, security, in_use}."""
        out = _run("nmcli", "-t", "-f", "IN-USE,SSID,SIGNAL,SECURITY",
                   "device", "wifi", "list", "--rescan", "no")
        networks = []
        seen = set()
        for line in out.splitlines():
            parts = line.split(":")
            if len(parts) < 4:
                continue
            in_use = parts[0].strip() == "*"
            ssid = parts[1].strip()
            if not ssid or ssid in seen:
                continue
            seen.add(ssid)
            try:
                signal = int(parts[2].strip())
            except ValueError:
                signal = 0
            security = parts[3].strip()
            networks.append({
                "ssid": ssid,
                "signal": signal,
                "security": security,
                "in_use": in_use,
            })
        networks.sort(key=lambda n: (-n["in_use"], -n["signal"]))
        return networks

    def connect(self, ssid):
        _run("nmcli", "device", "wifi", "connect", ssid, timeout=15)

    def disconnect(self):
        _run("nmcli", "device", "disconnect", "wlan0", timeout=5)


# ------------------------------------------------------------------ #
#  Bluetooth (bluetoothctl)                                            #
# ------------------------------------------------------------------ #
class BluetoothBackend:
    def is_powered(self):
        out = _run("bluetoothctl", "show")
        for line in out.splitlines():
            if "Powered:" in line:
                return "yes" in line.lower()
        return False

    def set_powered(self, on):
        if on:
            _run("rfkill", "unblock", "bluetooth")
            _run("bluetoothctl", "power", "on")
        else:
            _run("bluetoothctl", "power", "off")

    def get_devices(self):
        """Return list of dicts: {mac, name, connected, battery}."""
        out = _run("bluetoothctl", "devices", "Paired")
        devices = []
        for line in out.splitlines():
            m = re.match(r"Device\s+([0-9A-F:]+)\s+(.*)", line, re.IGNORECASE)
            if not m:
                continue
            mac = m.group(1)
            name = m.group(2).strip()
            info = _run("bluetoothctl", "info", mac)
            connected = False
            battery = None
            for iline in info.splitlines():
                iline = iline.strip()
                if iline.startswith("Connected:"):
                    connected = "yes" in iline.lower()
                if "Battery Percentage" in iline:
                    bm = re.search(r"\((\d+)\)", iline)
                    if bm:
                        battery = int(bm.group(1))
            devices.append({
                "mac": mac,
                "name": name,
                "connected": connected,
                "battery": battery,
            })
        devices.sort(key=lambda d: (-d["connected"], d["name"].lower()))
        return devices

    def connect_device(self, mac):
        _run("bluetoothctl", "connect", mac, timeout=10)

    def disconnect_device(self, mac):
        _run("bluetoothctl", "disconnect", mac, timeout=5)


# ------------------------------------------------------------------ #
#  Audio (wpctl / PipeWire)                                            #
# ------------------------------------------------------------------ #
class AudioBackend:
    def get_volume(self):
        """Return volume as 0-100+ float."""
        out = _run("wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@")
        m = re.search(r"(\d+\.\d+)", out)
        return round(float(m.group(1)) * 100) if m else 0

    def set_volume(self, percent):
        val = max(0.0, min(1.5, percent / 100.0))
        _run("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{val:.2f}")

    def is_muted(self):
        out = _run("wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@")
        return "[MUTED]" in out

    def toggle_mute(self):
        _run("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle")


# ------------------------------------------------------------------ #
#  Brightness (sysfs backlight)                                        #
# ------------------------------------------------------------------ #
class BrightnessBackend:
    DEVICE = Path("/sys/class/backlight/intel_backlight")

    def __init__(self):
        self._available = self.DEVICE.exists()
        self._max = 1
        if self._available:
            try:
                self._max = int((self.DEVICE / "max_brightness").read_text().strip())
            except Exception:
                self._available = False

    @property
    def available(self):
        return self._available

    def get_percentage(self):
        if not self._available:
            return 0
        try:
            raw = int((self.DEVICE / "brightness").read_text().strip())
            return round(raw / self._max * 100, 1)
        except Exception:
            return 0

    def set_percentage(self, pct):
        if not self._available:
            return
        raw = max(1, round(pct / 100 * self._max))
        path = self.DEVICE / "brightness"
        try:
            path.write_text(str(raw))
        except PermissionError:
            # Try brightnessctl as fallback (handles permissions via udev)
            try:
                subprocess.run(
                    ["brightnessctl", "set", f"{raw}"],
                    capture_output=True, timeout=3,
                )
            except Exception as e:
                logger.warning("Brightness write failed: %s", e)


# ------------------------------------------------------------------ #
#  Battery (UPowerGlib)                                                #
# ------------------------------------------------------------------ #
class BatteryBackend:
    def __init__(self):
        self._device = None
        self._available = False
        try:
            import gi
            gi.require_version("UPowerGlib", "1.0")
            from gi.repository import UPowerGlib
            client = UPowerGlib.Client.new()
            dev = client.get_display_device()
            if dev and dev.props.kind == UPowerGlib.DeviceKind.BATTERY:
                self._device = dev
                self._available = True
            else:
                for d in client.get_devices():
                    if "battery" in (d.get_object_path() or "").lower():
                        self._device = d
                        self._available = True
                        break
        except Exception as e:
            logger.debug("UPower not available: %s", e)

    @property
    def available(self):
        return self._available

    def get_info(self):
        """Return dict: {percentage, state, time_to_empty, time_to_full}."""
        if not self._available:
            return None
        try:
            self._device.refresh_sync(None)
        except Exception:
            pass
        pct = self._device.props.percentage
        state = self._device.props.state
        # state: 1=charging, 2=discharging, 4=fully-charged
        state_str = {1: "Charging", 2: "Discharging", 4: "Full"}.get(state, "Unknown")
        tte = self._device.props.time_to_empty  # seconds
        ttf = self._device.props.time_to_full
        return {
            "percentage": pct,
            "state": state_str,
            "time_to_empty": tte,
            "time_to_full": ttf,
        }


# ------------------------------------------------------------------ #
#  Night Light (Redshift)                                              #
# ------------------------------------------------------------------ #
class NightLightBackend:
    SCHEMA = "org.cinnamon.settings-daemon.plugins.color"
    KEY = "night-light-enabled"

    def is_active(self):
        out = _run("gsettings", "get", self.SCHEMA, self.KEY)
        return out.strip().lower() == "true"

    def enable(self, temp=4500):
        _run("gsettings", "set", self.SCHEMA, self.KEY, "true")

    def disable(self):
        _run("gsettings", "set", self.SCHEMA, self.KEY, "false")


# ------------------------------------------------------------------ #
#  Media (playerctl)                                                   #
# ------------------------------------------------------------------ #
class MediaBackend:
    ACTIVE_FILE = os.path.expanduser("~/.config/audio-router/active-player")

    def _player_args(self):
        try:
            with open(self.ACTIVE_FILE) as f:
                name = f.read().strip()
                if name:
                    return ["--player", name]
        except FileNotFoundError:
            pass
        return []

    def get_status(self):
        """Return dict or None: {player, artist, title, status}."""
        extra = self._player_args()
        cmd = ["playerctl"] + extra + [
            "metadata", "--format",
            "{{playerName}}\t{{artist}}\t{{title}}\t{{status}}",
        ]
        out = _run(*cmd)
        if not out:
            return None
        parts = out.split("\t", 3)
        if len(parts) < 4:
            return None
        return {
            "player": parts[0],
            "artist": parts[1],
            "title": parts[2],
            "status": parts[3],
        }

    def play_pause(self):
        _run("playerctl", *self._player_args(), "play-pause")

    def next(self):
        _run("playerctl", *self._player_args(), "next")

    def previous(self):
        _run("playerctl", *self._player_args(), "previous")


# ------------------------------------------------------------------ #
#  Airplane Mode (composite: WiFi + Bluetooth)                         #
# ------------------------------------------------------------------ #
class AirplaneModeBackend:
    def __init__(self, wifi, bluetooth):
        self._wifi = wifi
        self._bt = bluetooth
        self._active = False
        self._prev_wifi = True
        self._prev_bt = False

    @property
    def active(self):
        return self._active

    def toggle(self):
        if not self._active:
            self._prev_wifi = self._wifi.is_enabled()
            self._prev_bt = self._bt.is_powered()
            self._wifi.set_enabled(False)
            self._bt.set_powered(False)
            self._active = True
        else:
            self._wifi.set_enabled(self._prev_wifi)
            self._bt.set_powered(self._prev_bt)
            self._active = False


# ------------------------------------------------------------------ #
#  DND (local toggle — mutes notification sounds)                      #
# ------------------------------------------------------------------ #
class DNDBackend:
    def __init__(self):
        self._active = False

    @property
    def active(self):
        return self._active

    def toggle(self):
        self._active = not self._active
        # Try to pause Cinnamon notifications
        try:
            if self._active:
                subprocess.Popen(
                    ["dbus-send", "--session", "--type=method_call",
                     "--dest=org.Cinnamon",
                     "/org/Cinnamon", "org.freedesktop.DBus.Properties.Set",
                     "string:org.Cinnamon", "string:NotificationsEnabled",
                     "variant:boolean:false"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            else:
                subprocess.Popen(
                    ["dbus-send", "--session", "--type=method_call",
                     "--dest=org.Cinnamon",
                     "/org/Cinnamon", "org.freedesktop.DBus.Properties.Set",
                     "string:org.Cinnamon", "string:NotificationsEnabled",
                     "variant:boolean:true"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
        except Exception:
            pass


# ------------------------------------------------------------------ #
#  Power Saver (CPU governor toggle)                                   #
# ------------------------------------------------------------------ #
class PowerSaverBackend:
    def is_active(self):
        out = _run("powerprofilesctl", "get")
        return out.strip() == "power-saver"

    def toggle(self):
        target = "balanced" if self.is_active() else "power-saver"
        _run("powerprofilesctl", "set", target)


# ------------------------------------------------------------------ #
#  Hotspot (nmcli)                                                     #
# ------------------------------------------------------------------ #
class HotspotBackend:
    def is_active(self):
        out = _run("nmcli", "-t", "-f", "NAME,TYPE", "connection", "show", "--active")
        for line in out.splitlines():
            if "Hotspot" in line and "wireless" in line:
                return True
        return False

    def toggle(self):
        if self.is_active():
            _run("nmcli", "connection", "down", "Hotspot", timeout=10)
        else:
            _run("nmcli", "connection", "up", "Hotspot", timeout=10)



# ------------------------------------------------------------------ #
#  Microphone Mute (PulseAudio / PipeWire pactl)                     #
# ------------------------------------------------------------------ #
class MicBackend:
    def is_muted(self):
        out = _run("pactl", "get-source-mute", "@DEFAULT_SOURCE@")
        return "yes" in out.lower()

    def toggle(self):
        _run("pactl", "set-source-mute", "@DEFAULT_SOURCE@", "toggle")


# ------------------------------------------------------------------ #
#  Camera App Launcher                                               #
# ------------------------------------------------------------------ #
class CameraBackend:
    def open(self):
        import shutil, subprocess
        for app in ("cheese", "guvcview", "snapshot"):
            if shutil.which(app):
                subprocess.Popen([app], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True
        return False

# ------------------------------------------------------------------ #
#  Aggregated backends container                                       #
# ------------------------------------------------------------------ #
class Backends:
    """Container that initializes all backends."""

    def __init__(self):
        self.wifi = WiFiBackend()
        self.bluetooth = BluetoothBackend()
        self.audio = AudioBackend()
        self.brightness = BrightnessBackend()
        self.battery = BatteryBackend()
        self.night_light = NightLightBackend()
        self.media = MediaBackend()
        self.airplane = AirplaneModeBackend(self.wifi, self.bluetooth)
        self.dnd = DNDBackend()
        self.power_saver = PowerSaverBackend()
        self.hotspot = HotspotBackend()
        self.mic = MicBackend()
        self.camera = CameraBackend()
