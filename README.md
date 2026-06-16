# Manga Notifier 📖

Manga Notifier is a highly responsive, modern desktop application designed to track your favorite manga series and notify you instantaneously when new chapters are released. It features a custom smart-scraper that bypasses geo-restrictions and provides a sleek, dark-themed UI.

## ✨ Features
- **Real-Time Tracking**: Automatically polls for new chapter updates every 5 minutes.
- **Dynamic Scraping Engine**: Supports multiple popular reading platforms natively:
  - Bilibili Manga
  - Kuaikan Manhua
  - Kakao Webtoon
  - MangaDex
  - Tencent AC (ac.qq.com)
- **Smart Geo-Bypass**: Built-in Google Translate proxy fallback specifically designed to bypass Tencent AC's IP bans (e.g., in India) without requiring a VPN.
- **Persistent Storage**: Safely saves your tracked manga locally, ensuring you never lose your reading list.
- **Custom Title Editing**: Right-click any title to set a custom display name. The app remembers your changes permanently without interfering with scraper logic!
- **Modern UI**: A beautiful, tactile dark-mode interface with threaded chapter history and smooth animations.

## 🚀 Installation & Usage

You can download the compiled `.exe` release, which runs completely standalone!
Just download `MangaNotifier.exe` from the Releases tab and run it. It will automatically create its own data folder wherever you place it.

### Adding a Manga
1. Open Manga Notifier.
2. Click **+ Track Manga**.
3. Paste the URL of the manga page from one of the supported sites.
4. (Optional) Provide a custom display name.
5. Click **Add**. The app will immediately verify the link and fetch the latest chapters!

### Customizing Titles
If you want to change the display name of a manga you're already tracking, simply **Right-Click** its title on the main list to open the editor.

## 💻 Developer Setup
If you wish to compile the application from source:
```bash
# Clone the repository
git clone https://github.com/Ayaan3216/manga-notifier.git
cd manga-notifier

# Install dependencies
pip install requests beautifulsoup4 lxml winotify

# Run the app
python main.py
```

### Compiling to `.exe`
We use PyInstaller to compile the app into a standalone executable.
```bash
pip install pyinstaller Pillow
python -m PyInstaller MNv1.6.spec
```

## 📦 Version History

### **v1.6 (Current)**
- **Material You UI Overhaul:** Rebuilt the entire interface to adopt Android 16's Material Design 3 guidelines.
- **Smooth Pill Buttons:** Replaced legacy rigid buttons with dynamically generated, fully anti-aliased curved pill buttons using `Pillow`.
- **Floating Surface Cards:** Upgraded the manga tracking list from hard-lined separators to modern, padded floating cards.
- **Performance Fixes:** Introduced a smart UI debouncer (`_schedule_refresh`) that completely resolves the "Not Responding" application freezes during concurrent multi-threaded web scraping.
- **UI Bug Squashing:** Fixed modal height clipping, added custom `app_icon.ico` window decorations to dialogs, disabled background canvas scrolling when interacting with modals, and fixed duplicate-window spawns from button clicks.

### **v1.5**
- **Kakao Webtoon Support:** Implemented a new, efficient scraper utilizing Kakao's `gateway-kw` API to accurately track full chapter releases.
- **Automated Installers:** Introduced a robust `Install-MangaNotifier.ps1` PowerShell script and an Inno Setup `.iss` configuration for seamless upgrades that perfectly preserve user tracking lists.
- **About Modal:** Added a dedicated "ℹ" sheet featuring developer info, bug reporting links, and Patreon support.
- **Color Palettes:** Rolled out the first iteration of the deep "Default Dark" and "Dracula" modern palettes.

### **v1.4 & Earlier**
- Implemented the core multi-threaded background polling engine.
- Created the core GUI, including custom title editing and URL validation.
- Engineered a custom Google Translate proxy fallback to successfully bypass regional IP restrictions on Tencent AC.
- Initial support for Bilibili, Kuaikan, and MangaDex.

## 📜 Credits
**Developer:** Ayaan4uThere
**Feedback & Support:** schoolboy3216@gmail.com
