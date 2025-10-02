import os
import django
import requests
import json
from datetime import datetime
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Category, News


def save_news_from_json(json_file):
    BASE_URL = "https://data.daryo.uz/media/"

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data["data"]:
        title = item.get("title")
        description = item.get("short_content")
        image_path = item.get("img")  # masalan: 2025/10/02/xxxx.jpg
        category_name = item.get("category") or "Sport"  # JSONdan olamiz
        pub_date = item.get("date")  # 2025-10-02 10:11:53
        views_count = random.randint(1542, 2415)

        # 1️⃣ Category topiladi yoki yaratiladi
        category, _ = Category.objects.get_or_create(title=category_name)

        # 2️⃣ Rasmni yuklab olish
        img_path = None
        if image_path:
            print(image_path)
            image_url = BASE_URL + image_path
            print(f"web sayt >>>>>>>>>>>>>{image_url}")
            response = requests.get(image_url)
            if response.status_code == 200:
                filename = os.path.basename(image_path)  # faqat fayl nomi
                folder_path = "media/news"
                os.makedirs(folder_path, exist_ok=True)
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "wb") as img_file:
                    img_file.write(response.content)
                    print(response.content)
                img_path = f"news/{filename}"  # FileField uchun yo‘l

        # 3️⃣ Sana formatini to‘g‘ri parse qilish
        try:
            time_obj = datetime.strptime(pub_date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            time_obj = datetime.now()

        # 4️⃣ News yaratish
        News.objects.create(
            category=category,
            title=title,
            img=img_path if img_path else "default.jpg",
            descriptions=description,
            time=time_obj,
            see=views_count,
        )


if __name__ == "__main__":
    save_news_from_json("data.json")
