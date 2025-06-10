import requests
from bs4 import BeautifulSoup
import json
import random

# قائمة User-Agents يدوية لتجنب مشاكل المكتبات الخارجية
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
    "Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X)"
]

HEADERS = {'User-Agent': random.choice(USER_AGENTS)}

def fetch_3isk_biz():
    url = 'https://3isk.biz/category/turkish-series/'
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} 
            for a in soup.select('.post-title a')]

def fetch_bos_brstej():
    url = 'https://bos.brstej.com/category/1'
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} 
            for a in soup.select('.blog-entry .entry-title a')]

def fetch_shahid4u():
    url = 'https://shahid4u.free/category/المسلسلات-التركية/'
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} 
            for a in soup.select('.entry-title a')]

def fetch_3sk_tv():
    url = 'https://3sk.tv/category/مسلسلات-تركية/'
    res = requests.get(url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} 
            for a in soup.select('.post-box-title a')]

def get_all_episodes():
    all_eps = []
    for fetcher, name in [
        (fetch_3isk_biz, "3isk.biz"),
        (fetch_bos_brstej, "bos.brstej.com"),
        (fetch_shahid4u, "shahid4u.free"),
        (fetch_3sk_tv, "3sk.tv"),
    ]:
        try:
            eps = fetcher()
            print(f"✅ جلب {len(eps)} حلقة من {name}")
            all_eps.extend(eps)
        except Exception as e:
            print(f"❌ خطأ أثناء جلب الحلقات من {name}: {e}")

    # إزالة التكرارات إن احتوى المصدرين على روابط متشابهة
    unique = { ep['url']: ep for ep in all_eps }
    episodes = list(unique.values())

    with open('episodes.json', 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

    print(f"✅ تم حفظ {len(episodes)} حلقة فريدة في episodes.json")

if __name__ == "__main__":
    get_all_episodes()
