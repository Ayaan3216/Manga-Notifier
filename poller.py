"""
poller.py — Background polling engine for near-real-time chapter detection.

Strategy:
  • Default poll cycle: every 5 minutes (catches updates within ~5 min of release)
  • Each title is checked on every cycle — no staggering.
  • A separate "fast-check" path is exposed so the GUI can trigger instant checks.
  • A brief per-request delay (1 s) avoids hammering servers.
"""

import logging
import threading
import time
from typing import Callable

from scraper import scrape, get_session
from tracker import MangaTracker
from notifier import notify_new_chapter, notify_error

logger = logging.getLogger(__name__)

# Default poll interval in minutes — short enough for near-real-time detection.
DEFAULT_POLL_MINUTES = 5

# Minimum seconds between individual requests to avoid rate-limiting.
REQUEST_GAP_SECONDS = 1.5


class PollingEngine:
    """
    Runs a background thread that checks each tracked manga on a fixed interval.

    Near-real-time detection:
      - Default interval is 5 minutes.
      - On each cycle, every tracked manga is scraped sequentially.
      - The user can reduce the interval to as low as 1 minute.
      - force_check_now() fires an immediate out-of-band check.
    """

    def __init__(
        self,
        tracker: MangaTracker,
        interval_minutes: int = DEFAULT_POLL_MINUTES,
        on_new_chapter: Callable | None = None,
        on_status_update: Callable | None = None,
    ):
        self.tracker = tracker
        self.interval_minutes = max(1, interval_minutes)
        self.on_new_chapter = on_new_chapter
        self.on_status_update = on_status_update

        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None
        self._session = get_session()
        self._lock = threading.Lock()
        self._next_check_at: float = 0.0   # epoch time of next scheduled check

    # ── control ───────────────────────────────────────────────────────────────

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="manga-poller"
        )
        self._thread.start()
        logger.info("Polling engine started")

    def stop(self):
        self._stop_event.set()
        logger.info("Polling engine stopping…")

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def force_check_now(self):
        """Trigger an immediate check in a new thread (non-blocking)."""
        t = threading.Thread(
            target=self._check_all, daemon=True, name="manga-force-check"
        )
        t.start()

    def set_interval(self, minutes: int):
        self.interval_minutes = max(1, minutes)
        # Reset the next-check clock so the new interval takes effect immediately
        self._next_check_at = time.time() + self.interval_minutes * 60

    def seconds_until_next_check(self) -> float:
        remaining = self._next_check_at - time.time()
        return max(0.0, remaining)

    # ── core loop ─────────────────────────────────────────────────────────────

    def _run(self):
        """Main polling loop. Wakes up frequently to check if it's time."""
        # Immediate check on start
        self._check_all()
        self._next_check_at = time.time() + self.interval_minutes * 60

        # Sleep in 1-second ticks so stop_event is responsive
        while not self._stop_event.is_set():
            if time.time() >= self._next_check_at:
                self._check_all()
                self._next_check_at = time.time() + self.interval_minutes * 60
            self._stop_event.wait(1)

    def _check_all(self):
        with self._lock:
            entries = self.tracker.get_all()
            if not entries:
                self._emit_status("No titles being tracked.")
                return

            self._emit_status(f"Checking {len(entries)} title(s)…")

            for i, entry in enumerate(entries):
                if self._stop_event.is_set():
                    break
                self._check_one(entry.url)
                # Small gap between requests to be polite to servers
                if i < len(entries) - 1:
                    time.sleep(REQUEST_GAP_SECONDS)

            mins = self.interval_minutes
            self._emit_status(
                f"All checked. Next scan in {mins} min "
                f"({int(self.seconds_until_next_check())} s)."
            )

    def _check_one(self, url: str):
        entry = self.tracker.get(url)
        if entry is None:
            return

        display = entry.display_name
        self._emit_status(f"Checking: {display}…")

        try:
            info = scrape(url, self._session)

            if info.latest_chapter is None:
                logger.warning(f"No chapter found for {url}")
                self.tracker.record_error(url)
                return

            is_new = self.tracker.update_chapter(
                url,
                info.latest_chapter,
                info.title,
                info.cover_url,
            )

            if is_new:
                logger.info(
                    f"NEW chapter for {info.title}: "
                    f"Ch.{info.latest_chapter.number} — {info.latest_chapter.title}"
                )
                notify_new_chapter(
                    info.title,
                    f"Chapter {info.latest_chapter.number:.0f}: {info.latest_chapter.title}",
                    info.latest_chapter.url,
                )
                if self.on_new_chapter:
                    self.on_new_chapter(
                        url,
                        info.title,
                        info.latest_chapter.number,
                        info.latest_chapter.title,
                        info.latest_chapter.url,
                    )
            else:
                logger.debug(
                    f"No new chapter for {info.title} "
                    f"(latest stored: {entry.last_chapter_num})"
                )

        except ConnectionError as e:
            logger.error(f"Connection error for {url}: {e}")
            self.tracker.record_error(url)
            entry = self.tracker.get(url)
            if entry and entry.error_count >= 3:
                notify_error(display, str(e))

        except Exception as e:
            logger.exception(f"Unexpected error checking {url}")
            self.tracker.record_error(url)

    def _emit_status(self, message: str):
        logger.debug(f"[Status] {message}")
        if self.on_status_update:
            try:
                self.on_status_update(message)
            except Exception:
                pass
