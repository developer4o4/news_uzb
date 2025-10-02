from django.db import models
from django.utils import timezone
class Category(models.Model):
    title = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
class News(models.Model):
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=100)
    img = models.FileField(upload_to='media/news',default='salom.jpg')
    descriptions = models.TextField()
    time = models.DateField()
    see = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title