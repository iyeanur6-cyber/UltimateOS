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
```
## 🚀 Download & Release (`v1.0.0`)

The latest bootable ISO image is available on the **[UltimateOS Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/v1.0.0)**.

Because GitHub Releases limits individual file uploads to 2 GB, the **3.32 GB** ISO is distributed as two `.zip` parts alongside its SHA256 and MD5 checksums:
* `UltimateOS-22.3-amd64-part1.zip` (~1.8 GB)
* `UltimateOS-22.3-amd64-part2.zip` (~1.5 GB)
* `UltimateOS-22.3-amd64-sha256.txt`
* `UltimateOS-22.3-amd64-md5.txt`

---

## 📦 Step 1: Merge & Extract the ISO

1. Download **all four files** from the [Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/v1.0.0) into the same folder (for example, `~/Downloads`).
2. Open a terminal in that folder and run the following command to merge the two split `.zip` files and extract `UltimateOS-22.3-amd64.iso`:
   ```bash
   mv UltimateOS-22.3-amd64-part1.zip UltimateOS-22.3-amd64.z01 && \
   mv UltimateOS-22.3-amd64-part2.zip UltimateOS-22.3-amd64.zip && \
   zip -F UltimateOS-22.3-amd64.zip --out UltimateOS-full.zip && \
   unzip UltimateOS-full.zip
   ```
   Verify the integrity of the extracted ISO before flashing:

```Bash
sha256sum -c UltimateOS-22.3-amd64-sha256.txt
(You should see UltimateOS-22.3-amd64.iso: OK.)
```
💾 Step 2: Create a Bootable USB Drive
Use a USB flash drive with at least 8 GB of storage (all existing data on the USB will be erased):

On Linux (Recommended):

USB Image Writer (pre-installed on Linux Mint / UltimateOS): Open USB Image Writer, select UltimateOS-22.3-amd64.iso, choose your USB stick, and click Write.

Ventoy: Copy  UltimateOS-22.3-amd64.iso directly onto your Ventoy USB drive.

Terminal (dd):

```Bash
sudo dd if=UltimateOS-22.3-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync
(Replace /dev/sdX with your actual USB device from lsblk—do not append a partition number like 1.)
```
On Windows:

Use Rufus or BalenaEtcher, select UltimateOS-22.3-amd64.iso, choose your USB drive, and click Start / Flash.

🖥️ Step 3: Live Boot & Install UltimateOS
```Minimum & Recommended System Requirements
Component	Minimum	Recommended
Processor	64-bit x86_64 Dual-Core CPU	Quad-Core Intel / AMD CPU
RAM	2 GB	4 GB or more
Storage	20 GB free disk space	50 GB+ SSD
Graphics	1024×768 resolution	Hardware-accelerated GPU
```
Installation Walkthrough
Boot from USB: Restart your computer and press your motherboard's Boot Menu key (F12, F11, F2, Esc, or Del depending on your PC/laptop) to select your USB drive.

Test the Live Environment: UltimateOS boots directly into a full Live desktop session with Brave Browser, the ColorOS-inspired Quick Settings panel, and the WhiteSur Cinnamon UI ready to try before touching your hard drive.

Launch the Installer: Double-click the Install UltimateOS icon on the desktop.

Configure Installation:

Choose your Language and Keyboard Layout.

Check Install multimedia codecs if prompted.

On Installation type, select Erase disk and install UltimateOS for a clean single-OS setup, or Something else if you are dual-booting alongside Windows/Linux (create a / root partition formatted as ext4, plus an EFI System Partition if booting in UEFI mode).

Select your Timezone, create your Username and Password, and click Install Now.

Reboot: Once installation completes, click Restart Now, remove the USB flash drive when prompted, and press Enter to boot into your installed UltimateOS system.


---

### Push the Updated `README.md` to GitHub

Run this single line in your laptop terminal (`~/UltimateOS`) after adding the section above to `~/UltimateOS/README.md`:

```bash
cd ~/UltimateOS && git add README.md && git commit -m "Docs: Add v1.0.0 release download, extraction, and installation guide" && git push origin main
```

---

## 🧪 Tested Hardware & Verification Matrix

UltimateOS `v1.0.0` has been built, daily-driven on bare-metal hardware, and verified in QEMU/KVM Live ISO sessions:

| Test Environment | Hardware / VM Configuration | Idle RAM (`free -h`) | Verified Components |
| :--- | :--- | :--- | :--- |
| **Primary Host Laptop** | **Acer ALG (AL15G-53)**<br>• CPU: Intel Core i5-13420H<br>• GPU: NVIDIA GeForce RTX 3050 Mobile (4 GB VRAM)<br>• RAM: 16 GB DDR4<br>• Storage: 512 GB NVMe SSD | **~1.6 GiB** (full desktop + Quick Settings + BlurCinnamon active) | ColorOS Quick Settings (`#2aa6a6`), WhiteSur Dark theme & icons, Cinnamenu, BlurCinnamon, Brave Browser, custom keybindings, PipeWire/WirePlumber audio & brightness controls |
| **Live ISO Virtualization** | **QEMU / KVM (`x86_64`)**<br>• Boot Mode: BIOS / UEFI Live Session | **~1.6–1.8 GiB** (Live `squashfs` overlay) | Custom Neon Penguin Plymouth boot splash, Brave Browser default browser, WhiteSur icons, top bar, Terminal traffic-light window controls, Quick Settings daemon (`quick_settings.app`) |

### Known Notes in `v1.0.0` (Tracked for `v1.1.0`)
* **CSD / Flatpak Window Controls:** Native X11/GTK windows (such as Terminal) display left-aligned traffic lights (`close,minimize,maximize:`) out of the box. Certain Client-Side Decorated (CSD) apps like Nemo and sandboxed Flatpak apps may still default to right-side buttons in the Live session until overridden via `gsettings set org.cinnamon.desktop.interface gtk-decoration-layout 'close,minimize,maximize:'`.
* **Live Session System Tray:** In minimal VM configurations, `systray@cinnamon.org` may need to be enabled in Panel Applets if the Quick Settings tray icon is hidden on first Live boot.

---

## 🚀 Download Release (`v1.0.0`)

Download the release assets from the **[UltimateOS v1.0.0 Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/v1.0.0)**.

Because GitHub Releases enforces a 2 GB limit per file, the **3.32 GiB** bootable ISO is packaged as two `.zip` parts along with SHA256 and MD5 checksum files:
* `UltimateOS-22.3-amd64-part1.zip` (~1.8 GB)
* `UltimateOS-22.3-amd64-part2.zip` (~1.5 GB)
* `UltimateOS-22.3-amd64-sha256.txt`
* `UltimateOS-22.3-amd64-md5.txt`

---

## 📦 Step 1: Merge, Extract & Verify the ISO

1. Download **all four files** from the [Releases Page](https://github.com/iyeanur6-cyber/UltimateOS/releases/tag/v1.0.0) into the same directory (e.g., `~/Downloads`).
2. Open a terminal in that directory, reassemble the split `.zip` archive, and extract `UltimateOS-22.3-amd64.iso`:
   ```bash
   mv UltimateOS-22.3-amd64-part1.zip UltimateOS-22.3-amd64.z01 && \
   mv UltimateOS-22.3-amd64-part2.zip UltimateOS-22.3-amd64.zip && \
   zip -F UltimateOS-22.3-amd64.zip --out UltimateOS-full.zip && \
   unzip UltimateOS-full.zip
