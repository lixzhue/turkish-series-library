import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

def get_episodes():
    url = 'https://3isk.biz/category/turkish-series/'
    headers = {'User-Agent': UserAgent().random}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'lxml')

    # تعديل هذا الجزء حسب تنسيق الموقع
    episodes = []

    for item in soup.select('.post-title a'):
        episodes.append({
            'title': item.get_text(strip=True),
            'url': item['href']
        })

    with open('episodes.json', 'w', encoding='utf-8') as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    get_episodes()
