"""
notifier.py — Windows desktop notification dispatcher.
Uses winotify for native Windows toast notifications.
"""

import logging
import webbrowser
from pathlib import Path

logger = logging.getLogger(__name__)

# App icon path (bundled alongside the script)
ICON_PATH = str(Path(__file__).parent / "assets" / "icon.ico")


def _send_winotify(title: str, message: str, url: str = ""):
    """Send a Windows 10/11 toast notification via winotify."""
    try:
        from winotify import Notification, audio

        toast = Notification(
            app_id="Manga Notifier",
            title=title,
            msg=message,
            icon=ICON_PATH if Path(ICON_PATH).exists() else "",
            duration="short",
        )
        toast.set_audio(audio.Default, loop=False)

        if url:
            toast.add_actions(label="Open Chapter", launch=url)

        toast.show()
        return True
    except Exception as e:
        logger.warning(f"winotify failed: {e}")
        return False


def _send_messagebox_fallback(title: str, message: str, url: str = ""):
    """Fallback: use tkinter messagebox if winotify isn't available."""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.withdraw()
        full_msg = message + (f"\n\nOpen: {url}" if url else "")
        messagebox.showinfo(title, full_msg)
        root.destroy()
        if url:
            webbrowser.open(url)
    except Exception as e:
        logger.error(f"All notification methods failed: {e}")


def notify_new_chapter(manga_title: str, chapter_title: str, chapter_url: str = ""):
    """
    Send a new-chapter notification to the user.
    Tries winotify first, falls back to tkinter messagebox.
    """
    title = f"📖 New Chapter — {manga_title}"
    message = f"{chapter_title} is now available!"
    logger.info(f"Notifying: {title} | {message}")

    if not _send_winotify(title, message, chapter_url):
        _send_messagebox_fallback(title, message, chapter_url)


def notify_error(manga_title: str, error_msg: str):
    """Send a soft error notification (low priority)."""
    title = f"⚠ Manga Notifier — {manga_title}"
    message = f"Could not check for updates: {error_msg}"
    logger.warning(f"Error notification: {title} | {message}")
    _send_winotify(title, message)
