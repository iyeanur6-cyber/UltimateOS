#!/usr/bin/env bash
set -e
sudo apt update && sudo apt install -y curl git python3-gi gir1.2-gtk-3.0 gir1.2-ayatanaappindicator3-0.1 blueman rfkill wireplumber brightnessctl cheese
if ! command -v brave-browser >/dev/null 2>&1; then
  sudo curl -fsSL https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg -o /usr/share/keyrings/brave-browser-archive-keyring.gpg
  echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser-release.list
  sudo apt update && sudo apt install -y brave-browser
fi
sudo apt purge -y firefox firefox-locale-en && sudo apt autoremove -y
if false; then
fi
sudo apt purge -y firefox firefox-locale-en && sudo apt autoremove -y
if false; then
fi
sudo mkdir -p /opt/quick-settings-coloros && sudo cp -r ./quick-settings-coloros/* /opt/quick-settings-coloros/ && sudo cp ./bin/quick-settings-coloros /usr/local/bin/ && sudo chmod +x /usr/local/bin/quick-settings-coloros
mkdir -p ~/.themes ~/.icons ~/Pictures/Wallpapers ~/.config/autostart
cp -r ./themes/* ~/.themes/ 2>/dev/null || true
cp -r ./icons/* ~/.icons/ 2>/dev/null || true
cp ./wallpaper/* ~/Pictures/Wallpapers/ 2>/dev/null || true
printf '[Desktop Entry]\nType=Application\nName=UltimateOS Quick Settings\nExec=python3 /usr/local/bin/quick-settings-coloros\nX-GNOME-Autostart-enabled=true\n' > ~/.config/autostart/quick-settings-coloros.desktop
sed "s|\$HOME|$HOME|g" ./cinnamon-dconf.ini | dconf load /org/cinnamon/
WP=$(ls ~/Pictures/Wallpapers/default-wallpaper.* 2>/dev/null | head -n 1); [ -n "$WP" ] && gsettings set org.cinnamon.desktop.background picture-uri "file://$WP"
pkill -f "/usr/local/bin/quick-settings-coloros" 2>/dev/null || true; nohup python3 /usr/local/bin/quick-settings-coloros >/dev/null 2>&1 &
echo "UltimateOS Installed! Log out and back in to apply full UI."
