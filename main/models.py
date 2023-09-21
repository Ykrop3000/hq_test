from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    duration = models.PositiveIntegerField()  # в секундах
    products = models.ManyToManyField(Product)

class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class LessonViewHistory(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=0, blank=True)
    status = models.BooleanField(default=False)  # False - "Не просмотрено", True - "Просмотрено"
    last_change = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_change = timezone.now()
        super().save(*args, **kwargs)
