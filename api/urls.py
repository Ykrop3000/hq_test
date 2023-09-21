from django.urls import path
from .views import LessonListAPIView, ProductLessonListAPIView, ProductStatisticsAPIView

urlpatterns = [
    path('lessons/<int:product_id>/', ProductLessonListAPIView.as_view(), name='product-lesson-list'),
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('statistic/', ProductStatisticsAPIView.as_view(), name='statistic'),

]
