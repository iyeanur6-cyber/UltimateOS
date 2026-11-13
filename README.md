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
