from django.urls import path
from .views import *
urlpatterns = [
    path('',all_category,name="send_message"),
    path("search-suggest/", search_suggest, name="search_suggest"),
    path("news/<int:pk>/", news_detail, name="news_detail"),
]
