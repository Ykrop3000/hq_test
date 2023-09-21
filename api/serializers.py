from rest_framework import serializers
from rest_framework.utils import model_meta

from main.models import Lesson, LessonViewHistory


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonViewHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonViewHistory
        fields = '__all__'

