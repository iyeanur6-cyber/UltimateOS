# ColorOS Quick Settings — Glass / Navy Edition

This edition keeps the original system backends and Wi-Fi/Bluetooth detail views, while replacing the main UI with a translucent glassmorphism design:

- Deep navy background with lighter blue gradient toward the panel interior
- Frosted white/translucent surfaces (GTK3 compositor-friendly approximation of blur)
- Wi-Fi and Bluetooth remain the two large cards at the top
- Other quick controls become small circular buttons
- Color accents for common controls
- Media, brightness, volume, battery and existing backend functionality are retained

> GTK3 does not provide true backdrop-filter blur. The panel therefore uses translucent layers, gradients, borders and shadows to create the same visual glass effect under Cinnamon's compositor.

## Install on Linux Mint Cinnamon

### 1. Install dependencies

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-upowerglib-1.0 \
  network-manager bluez pipewire wireplumber playerctl redshift brightnessctl
```

### 2. Extract the ZIP

```bash
cd ~/Downloads
unzip coloros-quick-settings-ui-v2-glass.zip
cd quick-settings-coloros
```

### 3. Test without installing system-wide

Run from the project directory:

```bash
python3 -m quick_settings --debug
```

Keep this terminal open while testing. If it starts correctly you should see:

```text
Quick Settings ready
```

Click the tray icon to open the panel.

### 4. Stop an older copy before testing

If an earlier copy is already running:

```bash
pkill -f 'quick_settings' || true
```

Then start the new copy again.

### 5. Optional: create a permanent launcher

Once the UI is confirmed, install the project under `/opt`:

```bash
sudo rm -rf /opt/quick-settings-coloros
sudo cp -r ~/Downloads/quick-settings-coloros /opt/quick-settings-coloros
```

Create the launcher:

```bash
sudo tee /usr/local/bin/quick-settings-coloros >/dev/null <<'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/opt/quick-settings-coloros")
from quick_settings.__main__ import main
main()
EOF
sudo chmod +x /usr/local/bin/quick-settings-coloros
```

Test the installed copy:

```bash
quick-settings-coloros --debug
```

### 6. Start automatically with Cinnamon

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/quick-settings-coloros.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=ColorOS Quick Settings
Comment=Glass-style Quick Settings panel
Exec=/usr/local/bin/quick-settings-coloros
Terminal=false
X-GNOME-Autostart-enabled=true
NoDisplay=true
EOF
```

Log out/in or restart the launcher.

## Where to customize the UI

### Colors / glass effect

Edit:

```text
quick_settings/theme.py
```

The most important values are in `COLORS` and the `.qs-panel`, `.qs-wide-tile`, `.qs-round-tile` rules.

### Tile sizes and layout

Edit:

```text
quick_settings/widgets.py
quick_settings/panel.py
```

`ToggleTile` controls the circular tile appearance. `PanelWindow._build_main()` controls the 4-column layout.

### System functionality / backends

The original backend implementation is kept in:

```text
quick_settings/backends.py
```

Do not change it just for UI work. This separation makes future UI changes much easier.

## Rollback

If you want to return to the previous version:

```bash
sudo rm -f /usr/local/bin/quick-settings-coloros
rm -f ~/.config/autostart/quick-settings-coloros.desktop
sudo rm -rf /opt/quick-settings-coloros
```

Your original Cinnamon settings and system services are not modified by this project.
