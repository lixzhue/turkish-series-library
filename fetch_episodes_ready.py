import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import os
import re

ua = UserAgent()
HEADERS = {'User-Agent': ua.random}
EPISODES_FILE = 'episodes.json'

# مواقع الجلب
SOURCES = [
    ('bos.brstej.com', 'https://bos.brstej.com/category/1', '.blog-entry .entry-title a', '.blog-entry img'),
    ('3isk.biz', 'https://3isk.biz/category/turkish-series/', '.post-title a', None),
    ('shahid4u.free', 'https://shahid4u.free/category/المسلسلات-التركية/', '.entry-title a', None),
    ('3sk.tv', 'https://3sk.tv/category/مسلسلات-تركية/', '.post-box-title a', None),
]

def load_existing():
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def make_key(ep):
    return f"{ep['title']}|{ep['url']}"

def fetch_source(name, url, link_sel, img_sel):
    eps = []
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.content, 'lxml')
    for a in soup.select(link_sel):
        title = a.get_text(strip=True)
        href = a['href']
        full_url = href if href.startswith('http') else f"https://{name}{href}"
        img = None
        if img_sel:
            img_tag = a.find_previous(img_sel.split()[0])
            if img_tag and img_tag.has_attr('src'):
                img = img_tag['src']
        eps.append({
            'title': title,
            'url': full_url,
            'image': img,
            'description': None,    # يمكن إضافته لاحقًا
            'language': 'مدبلج' if 'مدبلج' in title else 'مترجم',
            'source': name
        })
    return eps

def main():
    existing = load_existing()
    existing_keys = { make_key(ep) for ep in existing }
    new_eps = []

    for name, url, link_sel, img_sel in SOURCES:
        try:
            fetched = fetch_source(name, url, link_sel, img_sel)
            for ep in fetched:
                key = make_key(ep)
                if key not in existing_keys:
                    existing_keys.add(key)
                    new_eps.append(ep)
        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")

    all_eps = existing + new_eps
    with open(EPISODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_eps, f, ensure_ascii=False, indent=2)

    print(f"✅ Added {len(new_eps)} new episodes. Total now: {len(all_eps)}")

if __name__ == '__main__':
    main()
