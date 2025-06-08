
import requests
from bs4 import BeautifulSoup
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def fetch_episodes_from_site(base_url):
    episodes = []
    try:
        response = requests.get(base_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.select(".episodes-list a")
        for item in items:
            title = item.get("title") or item.text.strip()
            url = item.get("href")
            if title and url:
                episodes.append({"title": title, "url": url})
    except Exception as e:
        print(f"خطأ أثناء جلب الحلقات من {base_url}: {e}")
    return episodes

def update_episodes_file(filename="episodes.json"):
    all_episodes = []
    sources = [
        "https://3isk.biz/category/turkish-series/",
        "https://bos.brstej.com/category/turkish-series/",
        "https://shahid4u.free/category/turkish-series/"
    ]
    for url in sources:
        episodes = fetch_episodes_from_site(url)
        all_episodes.extend(episodes)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(all_episodes, f, ensure_ascii=False, indent=2)
    print(f"تم تحديث الملف {filename} بعدد {len(all_episodes)} حلقة.")

if __name__ == "__main__":
    update_episodes_file()
