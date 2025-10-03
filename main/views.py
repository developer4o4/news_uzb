from django.shortcuts import render,get_object_or_404
from .models import Category,News
import random
import requests

def all_category(request):
    news = list(News.objects.all())
    finally_news = News.objects.order_by('-created_at')[:22]
    random_news_1 = random.sample(news, 5) if len(news) >= 5 else news
    random_news_2 = random.sample(news, 12) if len(news) >= 5 else news
    categories_with_news = []
    all_categorys = Category.objects.all()  # queryset → list
    categorys = random.sample(list(all_categorys), 8) 
    for category in all_categorys:
        news_list = News.objects.filter(category=category).order_by('-created_at')[:10]  # har bir kategoriyadan 10 ta
        categories_with_news.append({
            "category": category,
            "news": news_list
        })

    if request.method == "POST":
        matn = request.POST.get("message")
        phone = request.POST.get("phone")
        text = f"📩 Yangi murojaat:\n\n📝 Matn: {matn}\n📞 Telefon: {phone}"
        if not text:
            return render(request,'home.html',{"status": "error", "message": "Text yozing avval!"})

        url = f"https://api.telegram.org/bot8349177494:AAFdZh90_vpOSC3ZHagIcSSgpsNq7OvVZm4/sendMessage"
        payload = {
            "chat_id": -4985219832,
            "text": text
        }
        response = requests.post(url, data=payload)
        print(response.status_code)
        if response.status_code == 200:
            return render(request,'home.html',{"status": "ok", "message": "Yuborildi ✅"})
        else:
            return render(request,'home.html',{"status": "error", "message": "Xatolik ❌"})
    return render(request,'home.html',{
        "news":News.objects.all(),
        "random_news":random_news_1,
        "famous":random_news_2,
        "finally_news":finally_news,
        "all_category":categorys,
        "categories_with_news":categories_with_news
    })
def category_one(request,id):
    category = Category.objects.get(id=id)
    filtered_news = News.objects.filter(category=category)
    return render(request,'filtered_news.html',{"filtered_news":filtered_news})
from django.http import JsonResponse
def search_suggest(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        news = News.objects.filter(title__icontains=query).order_by("-created_at")[:5]
        results = [
            {
                "id": n.id,
                "title": n.title,
                "url": f"/news/{n.id}/"   # detail sahifaga URL
            } for n in news
        ]
    print(results)
    return JsonResponse({"results": results})   

def news_detail(request, pk):
    # id bo‘yicha yangilikni olish
    all_categorys = Category.objects.all()  # queryset → list
    categorys = random.sample(list(all_categorys), 8) 
    news = get_object_or_404(News, pk=pk)

    # Masalan: o‘xshash yangiliklar ham chiqarish mumkin
    related_news = News.objects.exclude(pk=pk).order_by("-created_at")[:5]

    context = {
        "news": news,
        "related_news": related_news,
        "all_category":categorys,
    }
    return render(request, "detail.html", context)