from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'name: {self.name} owner: {self.owner}'

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    duration = models.PositiveIntegerField()  # в секундах
    products = models.ManyToManyField(Product)
    def __str__(self):
        return f'name: {self.name}'

class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'product: {self.product.name} user: {self.user}'

class LessonViewHistory(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=0, blank=True)
    status = models.BooleanField(default=False)  # False - "Не просмотрено", True - "Просмотрено"
    last_change = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.last_change = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'lesson {self.lesson.name} user: {self.user}'