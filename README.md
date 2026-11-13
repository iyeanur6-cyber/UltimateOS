# UltimateOS (Linux Mint 22.3 Edition)

**UltimateOS** is a modern, lightweight desktop environment built on top of **Linux Mint 22.3 (Cinnamon)**—combining the rock-solid stability and official updates of Linux Mint with a custom **ColorOS-inspired translucent glass Quick Settings panel**, a clean top-bar layout, custom themes and icons, and **Brave Browser** pre-configured out of the box.

---

## ✨ Key Features

- **ColorOS-Style Quick Settings Panel:**
  - Translucent dark-glass control center with calm `#2aa6a6` teal active highlights and crisp high-contrast labels.
  - Interactive **Wi-Fi** and **Bluetooth** device drawers powered by `blueman-manager` with automatic `rfkill` soft-block clearing.
  - One-click toggles for **Night Light**, **Power Saver**, **Mute Mic**, **Camera (`cheese`)**, **Airplane Mode**, **Do Not Disturb**, and **Dark Mode**.
  - Unified brightness (`brightnessctl`) and PipeWire volume (`wpctl`) sliders with live media controls.
- **Modern Top-Bar Desktop Layout:**
  - Streamlined Cinnamon top panel with custom themes, icon packs, and curated wallpaper applied automatically via `dconf`.
- **Privacy-First Browser Setup:**
  - Automatically installs **Brave Browser** from its official APT repository and cleanly purges pre-installed Firefox to keep the system lean.
- **100% Official Mint Updates:**
  - Sits cleanly on top of standard Linux Mint 22.3 packages—Linux kernel, driver, and security updates from Mint's Update Manager work seamlessly without breaking your UI.
- **Zero Personal Data:**
  - Completely scrubbed of local usernames, browser profiles, passwords, or machine-specific keys—safe to clone and deploy on any fresh Mint 22.3 machine.

---

## 🚀 One-Command Installation

Run this single command in a fresh **Linux Mint 22.3 (Cinnamon)** terminal:

```bash
git clone [https://github.com/iyeanur6-cyber/UltimateOS.git](https://github.com/iyeanur6-cyber/UltimateOS.git) && cd UltimateOS && ./install.sh
```
After the script finishes:

Log out and log back in (or press Alt + F2, type r, and press Enter) to reload the Cinnamon desktop shell.

Click the Quick Settings icon in the top-right panel bar to open your control center.

📁 Repository Structure
```
UltimateOS/
├── quick-settings-coloros/   # Custom Python/GTK3 ColorOS Quick Settings source code
├── bin/                      # Executable launcher installed to /usr/local/bin/
├── themes/                   # Custom GTK and Cinnamon themes
├── icons/                    # Custom system icon packs
├── wallpaper/                # Default desktop wallpaper
├── cinnamon-dconf.ini        # Portable Cinnamon desktop layout & panel configuration
├── install.sh                # Automated one-command post-install setup script
└── README.md                 # Project documentation
```
🔄 Keeping Your Setup Synced
If you customize your panel or desktop layout further on your machine, sync your local changes back to GitHub anytime:
```
cd ~/UltimateOS && git pull origin main
```
📜 License & Base System
Built on top of Linux Mint 22.3 (Zena) and Ubuntu 24.04 LTS. All underlying system packages remain managed by official Linux Mint and Ubuntu repositories.
```
### Quick Step to Save on GitHub
1. Open `[https://github.com/iyeanur6-cyber/UltimateOS/edit/main/README.md](https://github.com/iyeanur6-cyber/UltimateOS/edit/main/README.md)` in Brave Browser.
2. Select all existing text (`Ctrl + A`), paste the block above (`Ctrl + V`), and click **Commit changes...** in the top-right corner.
3. *(Optional)* To pull this updated `README.md` back down to your local `~/UltimateOS` folder so your laptop stays synced with GitHub, run `cd ~/UltimateOS && git pull origin main` in your terminal.
