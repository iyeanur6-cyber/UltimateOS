#!/usr/bin/env bash
set -Eeuo pipefail

# Run as the desktop user, not with sudo. Privileged operations use sudo below.
if [ "$(id -u)" -eq 0 ]; then
    echo "Please run this installer as your normal desktop user: bash install.sh"
    exit 1
fi

ROOT="$(cd -- "$(dirname -- "$(readlink -f -- "$0")")" && pwd)"
if [ ! -d "$ROOT/quick-settings-coloros" ] || [ ! -f "$ROOT/cinnamon-dconf.ini" ]; then
    echo "ERROR: Run this installer from a complete UltimateOS source checkout."
    exit 1
fi

echo "==> Installing UltimateOS dependencies and everyday applications"
sudo apt update
sudo apt install -y \
    curl git python3 python3-gi \
    gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 \
    blueman rfkill wireplumber brightnessctl cheese \
    baobab zenity dconf-cli

echo "==> Installing Brave Browser from its official APT repository"
if ! command -v brave-browser >/dev/null 2>&1; then
    sudo install -d -m 755 /usr/share/keyrings
    sudo curl -fsSL \
        https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg \
        -o /usr/share/keyrings/brave-browser-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" \
        | sudo tee /etc/apt/sources.list.d/brave-browser-release.list >/dev/null
    sudo apt update
    sudo apt install -y brave-browser
fi

# Keep the project's stated browser choice, but do not run duplicate purge commands.
if dpkg -s firefox >/dev/null 2>&1 || dpkg -s firefox-locale-en >/dev/null 2>&1; then
    sudo apt purge -y firefox firefox-locale-en
    sudo apt autoremove -y
fi

echo "==> Deploying the ColorOS-inspired Quick Settings application"
sudo install -d -m 755 /opt/quick-settings-coloros
sudo cp -a "$ROOT/quick-settings-coloros/." /opt/quick-settings-coloros/
sudo install -m 755 "$ROOT/bin/quick-settings-coloros" /usr/local/bin/quick-settings-coloros

echo "==> Installing UltimateOS Cinnamon assets"
mkdir -p "$HOME/.themes" "$HOME/.icons" \
    "$HOME/.local/share/cinnamon/applets" \
    "$HOME/.local/share/cinnamon/extensions" \
    "$HOME/.config/autostart" "$HOME/Pictures/Wallpapers"

if [ -d "$ROOT/themes" ]; then
    cp -a "$ROOT/themes/." "$HOME/.themes/"
fi
if [ -d "$ROOT/icons" ]; then
    cp -a "$ROOT/icons/." "$HOME/.icons/"
fi

# Install only the applets/extensions referenced by the supplied Cinnamon profile.
for APPLET in "Cinnamenu@json" "coloros-control-center@sherlock"; do
    if [ -d "$ROOT/local-cinnamon/applets/$APPLET" ]; then
        cp -a "$ROOT/local-cinnamon/applets/$APPLET" \
            "$HOME/.local/share/cinnamon/applets/"
    fi
done

for EXTENSION in "BlurCinnamon@klangman" "cinnamon-dynamic-wallpaper@TobiZog"; do
    if [ -d "$ROOT/local-cinnamon/extensions/$EXTENSION" ]; then
        cp -a "$ROOT/local-cinnamon/extensions/$EXTENSION" \
            "$HOME/.local/share/cinnamon/extensions/"
    fi
done

echo "==> Applying the UltimateOS Cinnamon profile"
sed "s|\\\$HOME|$HOME|g" "$ROOT/cinnamon-dconf.ini" | dconf load /org/cinnamon/

# Apply macOS-style left-side window controls to Cinnamon and GTK applications.
gsettings set org.cinnamon.desktop.wm.preferences button-layout 'close,minimize,maximize:'
gsettings set org.gnome.desktop.wm.preferences button-layout 'close,minimize,maximize:'

# The selected UltimateOS wallpaper is bundled with the included dynamic-wallpaper
# extension. Deploying that extension first makes this path available on disk.
WALLPAPER="$HOME/.local/share/cinnamon/extensions/cinnamon-dynamic-wallpaper@TobiZog/5.4/res/images/included_image_sets/lake/9.jpg"
if [ -f "$WALLPAPER" ]; then
    gsettings set org.cinnamon.desktop.background picture-options 'zoom'
    gsettings set org.cinnamon.desktop.background picture-uri "file://$WALLPAPER"
else
    echo "WARNING: UltimateOS wallpaper asset was not found; leaving the current wallpaper unchanged."
fi

echo "==> Installing AI launcher and keyboard shortcut bindings"
sudo install -m 755 "$ROOT/bin/ultimate-ai.sh" /usr/local/bin/ultimate-ai.sh
dconf load /org/cinnamon/desktop/keybindings/ < "$ROOT/configs/cinnamon-keybindings.ini"

echo "Keyboard shortcuts:"
echo "  Gemini:  Super+Shift+G (or Copilot key + Shift+Super)"
echo "  ChatGPT: Super+Alt+Shift+C (or Copilot key + Alt+Shift+Super)"
echo "  Claude:  Super+Ctrl+Shift+A (or Copilot key + Ctrl+Shift+Super)"

echo "==> Installing Brave system-titlebar integration"
sudo install -m 755 "$ROOT/bin/ultimate-brave-setup" /usr/local/bin/ultimate-brave-setup
/usr/local/bin/ultimate-brave-setup
cat > "$HOME/.config/autostart/ultimate-brave-appearance.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=UltimateOS Brave Window Controls
Comment=Use Cinnamon window decorations in Brave Browser
Exec=/usr/local/bin/ultimate-brave-setup
OnlyShowIn=X-Cinnamon;
X-GNOME-Autostart-enabled=true
NoDisplay=true
EOF

echo "==> Registering the optional first-login setup wizard"
sudo install -m 755 "$ROOT/bin/ultimate-setup-wizard" /usr/local/bin/ultimate-setup-wizard
cat > "$HOME/.config/autostart/ultimate-setup-wizard.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=UltimateOS First-Login Setup
Comment=Choose optional applications for UltimateOS
Exec=/usr/local/bin/ultimate-setup-wizard
OnlyShowIn=X-Cinnamon;
X-GNOME-Autostart-enabled=true
NoDisplay=true
EOF

echo "==> Installing the Hardware Fan & RGB Advisor"
sudo install -m 755 "$ROOT/bin/ultimate-hw-advisor" /usr/local/bin/ultimate-hw-advisor

# Add the advisor to Mint Welcome when the expected upstream insertion point exists.
# Keep a one-time backup so Mint Welcome can be restored if needed.
MINT_WELCOME="/usr/lib/linuxmint/mintwelcome/mintwelcome.py"
if [ -f "$MINT_WELCOME" ]; then
    sudo cp -n "$MINT_WELCOME" "$MINT_WELCOME.ultimateos-backup" || true
    sudo python3 - "$MINT_WELCOME" <<'PYEOF'
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
try:
    code = path.read_text()
    if "ultimate-hw-advisor" not in code and "mintdrivers" in code:
        snippet = (
            '        self.add_first_step("Fan & RGB Control Advisor", '
            '"Find third-party open-source fan and RGB control projects for your laptop or PC.", '
            '"preferences-system", "/usr/local/bin/ultimate-hw-advisor")'
        )
        lines = code.splitlines()
        for index, line in enumerate(lines):
            if "mintdrivers" in line:
                lines.insert(index + 1, snippet)
                path.write_text("\n".join(lines) + "\n")
                break
except (OSError, UnicodeError) as error:
    print(f"WARNING: Could not add the Hardware Advisor to Mint Welcome: {error}")
PYEOF
fi

echo "==> Registering Quick Settings autostart"
cat > "$HOME/.config/autostart/quick-settings-coloros.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=UltimateOS Quick Settings
Exec=python3 /opt/quick-settings-coloros
X-GNOME-Autostart-enabled=true
OnlyShowIn=X-Cinnamon;
EOF

# Restart only this application's process, without matching this installer shell.
pkill -f '[q]uick-settings-coloros' 2>/dev/null || true
nohup python3 /opt/quick-settings-coloros >/dev/null 2>&1 &

echo
echo "UltimateOS installation completed."
echo "The first-login wizard will appear at the next Cinnamon login."
echo "Log out and back in to apply the complete desktop configuration."
