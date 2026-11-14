# UltimateOS (Linux Mint 22.3 Edition)

**Dream • Customize • Use** — **UltimateOS** is a modern, lightweight desktop distribution built on **Linux Mint 22.3 (*Zena* / Ubuntu 24.04 LTS base)** with the Cinnamon desktop environment. It combines the rock-solid stability and official updates of Linux Mint with a custom **ColorOS-inspired translucent glass Quick Settings panel**, custom Neon Penguin Plymouth boot branding, a streamlined top-bar layout, WhiteSur themes and icons, and **Brave Browser** pre-installed out of the box.

---

## ✨ Key Features

- **ColorOS-Style Quick Settings Panel:**
  - Translucent dark-glass control center with calm `#2aa6a6` teal active highlights and crisp high-contrast labels.
  - Interactive **Wi-Fi** and **Bluetooth** device drawers powered by `blueman-manager` with automatic `rfkill` soft-block clearing.
  - One-click toggles for **Night Light**, **Power Saver**, **Mute Mic**, **Camera (`cheese`)**, **Airplane Mode**, **Do Not Disturb**, and **Dark Mode**.
  - Unified brightness (`brightnessctl`) and PipeWire volume (`wpctl`) sliders with live media controls.
- **Modern Top-Bar Desktop Layout:**
  - Streamlined Cinnamon top panel with Cinnamenu, BlurCinnamon, WhiteSur themes/icons, and curated wallpaper applied automatically via `dconf`.
- **Privacy-First Browser Setup:**
  - Pre-installs **Brave Browser** from its official APT repository and cleanly removes pre-installed Firefox to keep the base image lean.
- **100% Official Mint & Ubuntu Updates:**
  - Built cleanly on standard Linux Mint 22.3 packages—Linux kernel, driver, and security updates from Mint's Update Manager work seamlessly without breaking your UI.
- **Zero Personal Data:**
  - Completely scrubbed of local usernames, browser profiles, passwords, or machine-specific keys.

---

## 🧪 Tested Hardware & Performance Footprint

UltimateOS `v1.0.0` has been built, daily-driven on bare-metal hardware, and verified in QEMU/KVM Live ISO sessions:

| Test Environment | Hardware / VM Configuration | Idle RAM (`free -h`) | Verified Components |
| :--- | :--- | :--- | :--- |
| **Primary Host Laptop** | **Acer ALG (AL15G-53)**<br>• CPU: Intel Core i5-13420H<br>• GPU: NVIDIA GeForce RTX 3050 Mobile (4 GB VRAM)<br>• RAM: 16 GB DDR4<br>• Storage: 512 GB NVMe SSD | **~1.6 GiB** (full desktop + Quick Settings + BlurCinnamon active) | ColorOS Quick Settings (`#2aa6a6`), WhiteSur Dark theme & icons, Cinnamenu, BlurCinnamon, Brave Browser, custom keybindings, PipeWire/WirePlumber audio & brightness controls |
| **Live ISO Virtualization** | **QEMU / KVM (`x86_64`)**<br>• Boot Mode: BIOS / UEFI Live Session | **~1.6–1.8 GiB** (Live `squashfs` overlay) | Custom Neon Penguin Plymouth boot splash, Brave Browser default browser, WhiteSur icons, top bar, Terminal traffic-light window controls, Quick Settings daemon (`quick_settings.app`) |

### System Requirements

| Component | Minimum | Recommended |
| :--- | :--- | :--- |
| **Processor** | 64-bit x86_64 Dual-Core CPU | Quad-Core Intel / AMD CPU |
| **RAM** | 2 GB *(~1.6 GiB idle footprint)* | 4 GB or more |
| **Storage** | 20 GB free disk space | 50 GB+ SSD |
| **Graphics** | 1024×768 resolution | Hardware-accelerated GPU |

### Known Notes in `v1.0.0` (Tracked for `v1.1.0`)
- **CSD / Flatpak Window Controls:** Native X11/GTK windows (such as Terminal) display left-aligned traffic lights (`close,minimize,maximize:`) out of the box. Client-Side Decorated (CSD) apps like Nemo and sandboxed Flatpak apps may still default to right-side buttons in the Live session until overridden via `gsettings set org.cinnamon.desktop.interface gtk-decoration-layout 'close,minimize,maximize:'`.
- **Live Session System Tray:** In minimal VM configurations, `systray@cinnamon.org` may need to be enabled in Panel Applets if the Quick Settings tray icon is hidden on first Live boot.

---

## 🚀 Download Release (`v1.0.0`)

Download the release assets from the **[UltimateOS v1.0.0 Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/untagged-e444e23c43ad0dfec933)**.

Because GitHub Releases enforces a 2 GB limit per file, the **3.32 GiB** bootable ISO is distributed as two `.zip` parts alongside its SHA256 and MD5 checksum files:
- `UltimateOS-22.3-amd64-part1.zip` (~1.8 GB)
- `UltimateOS-22.3-amd64-part2.zip` (~1.5 GB)
- `UltimateOS-22.3-amd64-sha256.txt`
- `UltimateOS-22.3-amd64-md5.txt`

---

## 📦 Step 1: Merge, Extract & Verify the ISO

1. Download **all four files** from the [Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/untagged-e444e23c43ad0dfec933) into the same folder (for example, `~/Downloads`).
2. Open a terminal in that folder, merge the two split `.zip` parts, and extract `UltimateOS-22.3-amd64.iso`:
   ```bash
   mv UltimateOS-22.3-amd64-part1.zip UltimateOS-22.3-amd64.z01 && \
   mv UltimateOS-22.3-amd64-part2.zip UltimateOS-22.3-amd64.zip && \
   zip -F UltimateOS-22.3-amd64.zip --out UltimateOS-full.zip && \
   unzip UltimateOS-full.zip
