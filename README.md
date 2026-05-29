# Manga Notifier 📖

Manga Notifier is a highly responsive, modern desktop application designed to track your favorite manga series and notify you instantaneously when new chapters are released. It features a custom smart-scraper that bypasses geo-restrictions and provides a sleek, dark-themed UI.

## ✨ Features
- **Real-Time Tracking**: Automatically polls for new chapter updates every 5 minutes.
- **Dynamic Scraping Engine**: Supports multiple popular reading platforms natively:
  - Bilibili Manga
  - Kuaikan Manhua
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
pip install pyinstaller
python -m PyInstaller --noconsole --onefile --name MangaNotifier --icon=data/assets/mangadex.ico --add-data "data/assets;data/assets" main.py
```

## 📜 Credits
**Developer:** Ayaan4uThere
**Feedback & Support:** schoolboy3216@gmail.com
