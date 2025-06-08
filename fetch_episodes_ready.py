
import requests
from bs4 import BeautifulSoup
import json
import re
import os

EPISODES_FILE = "episodes.json"
BASE_URL = "https://3isk.biz"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def is_ad_link(link):
    return any(bad in link for bad in ["ads", "doubleclick", "popads", "banner", "redirect"])

def fetch_series_links():
    print("جلب روابط المسلسلات من الصفحة الرئيسية...")
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    series_links = []
    for a in soup.select("a"):
        href = a.get("href")
        if href and "/مسلسل" in href and not is_ad_link(href):
            full_url = href if href.startswith("http") else BASE_URL + href
            if full_url not in series_links:
                series_links.append(full_url)
    return series_links[:20]

def fetch_episodes(series_url):
    print(f"جلب الحلقات من: {series_url}")
    res = requests.get(series_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.text.strip().split("–")[0] if title_tag else "مسلسل غير معرف"
    episodes = []
    for a in soup.select("a"):
        href = a.get("href")
        if href and "/episode" in href and not is_ad_link(href):
            ep_url = href if href.startswith("http") else BASE_URL + href
            if ep_url not in episodes:
                episodes.append(ep_url)
    return {"title": title, "episodes": episodes}

def save_data(data):
    with open(EPISODES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"تم حفظ {len(data)} مسلسل في ملف {EPISODES_FILE}")

def main():
    all_series = fetch_series_links()
    data = []
    for url in all_series:
        try:
            series_data = fetch_episodes(url)
            if series_data["episodes"]:
                data.append(series_data)
        except Exception as e:
            print(f"خطأ أثناء جلب {url}: {e}")
    save_data(data)

if __name__ == "__main__":
    main()
