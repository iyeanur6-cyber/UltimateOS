# ColorOS-inspired Quick Settings for Cinnamon

A GTK3 quick-settings panel for Linux Mint/Cinnamon, redesigned around the supplied ColorOS/Android-style reference: rounded cards, circular icons, large media card, sliders, active-state surfaces, and a dark modern layout.

## Backend strategy

The existing system backends are intentionally retained: NetworkManager/nmcli for Wi-Fi, BlueZ/bluetoothctl for Bluetooth, PipeWire/wpctl for audio, sysfs/brightnessctl for brightness, UPower for battery, playerctl for media, Redshift for night light, and the existing composite toggles. The main changes are the presentation layer (`panel.py`, `widgets.py`, `theme.py`).

## Install dependencies

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-upowerglib-1.0 \
  network-manager bluez pipewire wireplumber playerctl redshift brightnessctl
```

## Run from the extracted folder

```bash
cd quick-settings-coloros
python3 -m quick_settings --debug
```

If running directly from a source checkout is inconvenient, install it under `/opt` and create a launcher similar to the original project.

## Notes

- The panel is a Cinnamon/GTK3 desktop panel, not a mobile shell.
- Wi-Fi and Bluetooth detail pages from the original project are kept.
- The design intentionally uses Linux-native symbolic icons where available.
- `BrightnessBackend` still targets the original `intel_backlight` path; change it if your machine exposes another backlight device.
