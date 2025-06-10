import requests
from bs4 import BeautifulSoup
import json
import random

# قائمة user agents لتجنب استخدام fake_useragent الذي يسبب مشاكل في GitHub Actions
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)"
]

def get_episodes():
    url = 'https://3isk.biz/category/turkish-series/'
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ فشل في جلب الصفحة: {e}")
        return

    soup = BeautifulSoup(response.content, 'lxml')

    episodes = []

    for item in soup.select('.post-title a'):
        episodes.append({
            'title': item.get_text(strip=True),
            'url': item['href']
        })

    with open('episodes.json', 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

    print(f"✅ تم استخراج {len(episodes)} حلقة وحفظها في episodes.json")

if __name__ == "__main__":
    get_episodes()
