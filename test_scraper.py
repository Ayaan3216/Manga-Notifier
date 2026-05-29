import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from scraper import scrape

test_urls = [
    ('Kuaikan Manga', 'https://www.kuaikanmanhua.com/web/topic/21809/'),
    ('Bilibili Manga', 'https://manga.bilibili.com/detail/mc35917'),
    ('MangaDex', 'https://mangadex.org/title/c52b2ce3-7f95-469c-96b0-479524fb7a1a'),  # Chainsaw Man
]

for name, url in test_urls:
    print(f"=== {name} ===")
    print(f"URL: {url}")
    try:
        info = scrape(url)
        print(f"Title: {info.title}")
        if info.latest_chapter:
            ch = info.latest_chapter
            print(f"Latest: Ch.{ch.number} — {ch.title}")
            print(f"URL: {ch.url}")
        else:
            print("No chapter found")
    except Exception as e:
        print(f"ERROR: {e}")
    print()
