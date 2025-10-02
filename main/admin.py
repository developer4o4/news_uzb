from django.contrib import admin
from .models import News, Category
# Register your models here.
admin.site.register(Category)
admin.site.register(News)