import json
import os
import time
import cloudscraper
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# ملف النتائج
EPISODES_FILE = 'episodes.json'

# وكيل المستخدم العشوائي
ua = UserAgent()
# cloudscraper session (لتجاوز الحماية)
scraper = cloudscraper.create_scraper(browser={'custom': ua.random})

# المصادر: (اسم، رابط الصفحة، محدد العنصر للعناوين)
SOURCES = [
    ('3isk', 'https://3isk.biz/category/turkish-series/', '.post-title a'),
    ('bos', 'https://bos.brstej.com/category/1', '.blog-entry .entry-title a'),
    ('shahid4u', 'https://shahid4u.free/category/المسلسلات-التركية/', '.entry-title a'),
    ('3sk', 'https://3sk.tv/category/مسلسلات-تركية/', '.post-box-title a'),
]


def load_existing():
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_episodes(eps):
    with open(EPISODES_FILE, 'w', encoding='utf-8') as f:
        json.dump(eps, f, ensure_ascii=False, indent=2)


def make_key(ep):
    return f"{ep['title']}|{ep['url']}"


def fetch_from(source_name, url, selector):
    print(f"🔍 جلب من {source_name}...")
    eps = []
    try:
        res = scraper.get(url, timeout=15)
        soup = BeautifulSoup(res.text, 'lxml')
        for a in soup.select(selector):
            title = a.get_text(strip=True)
            href = a.get('href')
            if not href:
                continue
            full_url = href if href.startswith('http') else f"https://{source_name}.biz{href}"  # adjust
            eps.append({'title': title, 'url': full_url, 'source': source_name})
    except Exception as e:
        print(f"⚠️ خطأ في {source_name}: {e}")
    return eps


def main():
    existing = load_existing()
    existing_keys = {make_key(ep) for ep in existing}
    new_eps = []

    for name, page_url, sel in SOURCES:
        fetched = fetch_from(name, page_url, sel)
        time.sleep(2)
        for ep in fetched:
            key = make_key(ep)
            if key not in existing_keys:
                existing_keys.add(key)
                new_eps.append(ep)

    all_eps = existing + new_eps
    save_episodes(all_eps)
    print(f"✅ تم إضافة {len(new_eps)} حلقات جديدة. المجموع: {len(all_eps)}")


if __name__ == '__main__':
    main()
