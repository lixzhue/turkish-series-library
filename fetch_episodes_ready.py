import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

HEADERS = {'User-Agent': UserAgent().random}

def fetch_3isk_biz():
    url = 'https://3isk.biz/category/turkish-series/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} for a in soup.select('.post-title a')]

def fetch_bos_brstej():
    url = 'https://bos.brstej.com/category/1'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} for a in soup.select('.blog-entry .entry-title a')]

def fetch_shahid4u():
    url = 'https://shahid4u.free/category/المسلسلات-التركية/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} for a in soup.select('.entry-title a')]

def fetch_3sk_tv():
    url = 'https://3sk.tv/category/مسلسلات-تركية/'
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    return [{'title': a.get_text(strip=True), 'url': a['href']} for a in soup.select('.post-box-title a')]

def get_all_episodes():
    episodes = []
    try:
        episodes += fetch_3isk_biz()
    except Exception as e:
        print("❌ Error fetching from 3isk.biz:", e)

    try:
        episodes += fetch_bos_brstej()
    except Exception as e:
        print("❌ Error fetching from bos.brstej.com:", e)

    try:
        episodes += fetch_shahid4u()
    except Exception as e:
        print("❌ Error fetching from shahid4u.free:", e)

    try:
        episodes += fetch_3sk_tv()
    except Exception as e:
        print("❌ Error fetching from 3sk.tv:", e)

    with open('episodes.json', 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_all_episodes()
