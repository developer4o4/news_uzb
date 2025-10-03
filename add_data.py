import os
import django
import requests
import json
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Category, News


def fetch_news():
    url = "https://kun.uz/news/list?f=latest&l=5"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
        "X-Requested-With": "XMLHttpRequest",   # 🔑 majburiy
        "Accept": "application/json",           # 🔑 JSON deb qabul qilsin
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()   # endi JSON qaytadi


def save_news_from_api():
    data = fetch_news()
    print(data)
    print(len(data.get("news")))
    for item in data.get("news", []):
        title = item.get("title")
        description = item.get("description")
        image_url = item.get("image")
        category_name = item.get("category_name")
        pub_date = item.get("pub_date")  # misol: 03.10.2025
        views_count = item.get("views_count", 0)

        # Yangilik bor-yo‘qligini tekshirish
        if News.objects.filter(title=title).exists():
            continue

        # Category topiladi yoki yaratiladi
        category, _ = Category.objects.get_or_create(title=category_name)

        # Sana formatini to‘g‘ri parse qilish
        try:
            time_obj = datetime.strptime(pub_date, "%d.%m.%Y")
        except ValueError:
            time_obj = datetime.now()

        # News yaratish
        News.objects.create(
            category=category,
            title=title,
            descriptions=description,
            img=image_url or "default.jpg",  # hozircha link saqlaymiz
            time=time_obj,
            see=views_count,
        )
        print(f"✅ Yangi yangilik qo‘shildi: {title}")



import time
if __name__ == "__main__":
    while True:
        save_news_from_api()
        print("⏳ Keyingi tekshirishdan oldin 5 minut kutyapmiz...")
        time.sleep(10)  # 300 sekund = 5 minut
