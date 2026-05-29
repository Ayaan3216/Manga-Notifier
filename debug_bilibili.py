import requests, re, sys, io, json
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HEADERS_MOBILE = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

comic_id = 35917

mob_r = requests.get(
    f'https://manga.bilibili.com/m/detail/mc{comic_id}',
    headers=HEADERS_MOBILE, timeout=15
)
msoup = BeautifulSoup(mob_r.text, 'lxml')
print(f"Title: {msoup.find('title').get_text()}")

# Get the big inline script [3]
scripts = msoup.find_all('script')
big_inline = None
for s in scripts:
    if not s.get('src') and len(s.get_text()) > 10000:
        big_inline = s.get_text()
        break

if big_inline:
    print(f"Found inline JSON: {len(big_inline)} chars")
    
    # Parse as JSON
    try:
        data = json.loads(big_inline)
        print(f"Top-level keys: {list(data.keys())[:15]}")
        
        # Search for episode/chapter data
        def find_keys(d, targets, path=''):
            if isinstance(d, dict):
                for k, v in d.items():
                    new_path = f"{path}.{k}" if path else k
                    if any(t in k.lower() for t in targets):
                        print(f"  FOUND: {new_path} = {repr(v)[:100]}")
                    find_keys(v, targets, new_path)
            elif isinstance(d, list) and len(d) > 0:
                find_keys(d[0], targets, f"{path}[0]")
        
        print("\nSearching for ep/chapter keys:")
        find_keys(data, ['ep_list', 'episode', 'chapter', 'ord', 'last_ord', 'total', 'comic_id', 'title'])
        
    except json.JSONDecodeError as e:
        print(f"Not pure JSON: {e}")
        # Try to find JSON within the script text
        # The script starts with {... let's look at structure
        print("First 500 chars:", big_inline[:500])
        
        # Look for key manga data patterns
        for pat in [r'"ep_list":\[', r'"comic_id":\d+', r'"last_ord":\d+', r'"title":"[^"]+"']:
            m = re.search(pat, big_inline)
            if m:
                idx = m.start()
                print(f"\nPattern '{pat}' found at {idx}:")
                print(big_inline[max(0,idx-50):idx+300])
