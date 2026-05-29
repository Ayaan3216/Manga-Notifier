"""
Extract latest chapter from Kuaikan NUXT data.
"""
import requests, re, sys, io
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}

def split_js_args(args_str: str) -> list:
    args, current, depth, in_str, esc = [], [], 0, False, False
    sc = ''
    for c in args_str:
        if esc:
            current.append(c)
            esc = False
            continue
        if in_str:
            if c == '\\':
                esc = True
            elif c == sc:
                in_str = False
            current.append(c)
        else:
            if c in ('"', "'"):
                in_str = True
                sc = c
                current.append(c)
            elif c in ('(', '[', '{'):
                depth += 1
                current.append(c)
            elif c in (')', ']', '}'):
                depth -= 1
                current.append(c)
            elif c == ',' and depth == 0:
                args.append(''.join(current).strip())
                current = []
            else:
                current.append(c)
    if current:
        args.append(''.join(current).strip())
    return args

def decode_js_string(val: str) -> str:
    inner = val[1:-1]
    inner = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), inner)
    return inner

r = requests.get('https://www.kuaikanmanhua.com/web/topic/21809/', headers=HEADERS, timeout=15)
soup = BeautifulSoup(r.text, 'lxml')
big_script = soup.find_all('script')[2].get_text()

params_m = re.match(r'window\.__NUXT__=\(function\(([^)]+)\)', big_script)
params = [p.strip() for p in params_m.group(1).split(',')]
last_brace_paren = big_script.rfind('}(')
args_end = big_script.rfind('))')
args_str = big_script[last_brace_paren + 2: args_end]
args_raw = split_js_args(args_str)

var_map = {}
for p, a in zip(params, args_raw):
    val = a.strip()
    if val == 'true': var_map[p] = True
    elif val == 'false': var_map[p] = False
    elif val in ('null', 'undefined', 'void 0'): var_map[p] = None
    elif (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        var_map[p] = decode_js_string(val)
    else:
        try: var_map[p] = int(val)
        except ValueError:
            try: var_map[p] = float(val)
            except ValueError: var_map[p] = val

body_start = big_script.index('{', big_script.index(')'))
body = big_script[body_start:last_brace_paren]

# Find the comics list: {id:VAR,title:VAR,cover_image_url:VAR,...}
# In the body after `comics:[`
# Each comic is: {id:N,title:STR,...,seq_num:N,...}
comic_pattern = re.compile(
    r'\{id:(\w+),title:(\w+),cover_image_url:(\w+)[^}]*?seq_num:(\w+)[^}]*?\}'
)
entries = comic_pattern.findall(body)

if entries:
    print(f"Found {len(entries)} chapter entries")
    print("\nAll chapters (showing last 10):")
    chapter_data = []
    for e in entries:
        ch_id = var_map.get(e[0])
        ch_title = var_map.get(e[1])
        ch_seq = var_map.get(e[3])
        chapter_data.append((ch_seq, ch_title, ch_id))
    
    chapter_data.sort(key=lambda x: x[0] if isinstance(x[0], (int, float)) else 0)
    for seq, title, cid in chapter_data[-10:]:
        print(f"  seq={seq}, title={repr(title)}, id={cid}")
    
    if chapter_data:
        latest = chapter_data[-1]
        print(f"\nLATEST: seq={latest[0]}, title={repr(latest[1])}, id={latest[2]}")
        print(f"  URL: https://www.kuaikanmanhua.com/web/comic/{latest[2]}/")
else:
    # Try without seq_num
    comic_pattern2 = re.compile(r'\{id:(\w+),title:(\w+),cover_image_url:(\w+)')
    entries2 = comic_pattern2.findall(body)
    print(f"Found {len(entries2)} entries (without seq_num)")
    if entries2:
        print("Last 5:")
        for e in entries2[-5:]:
            print(f"  id={var_map.get(e[0])}, title={repr(var_map.get(e[1]))}")
