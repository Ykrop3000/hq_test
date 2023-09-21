from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Count, Sum, ExpressionWrapper, F, Q
from django.db.models.functions import Coalesce
from django.db.models import FloatField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from main.models import Lesson, ProductAccess, LessonViewHistory, Product
from .serializers import LessonSerializer, LessonViewHistorySerializer


class LessonListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        product_access_list = ProductAccess.objects.select_related('product').filter(user=user)
        products = [access.product for access in product_access_list]
        lesson_list = Lesson.objects.filter(products__in=products)

        serialized_lessons = LessonSerializer(lesson_list, many=True).data

        lesson_view_history = LessonViewHistory.objects.filter(lesson__in=lesson_list, user=user).order_by('lesson', 'duration')
        lesson_view_history_dict = {history.lesson_id: history for history in lesson_view_history}

        for lesson in serialized_lessons:
            history = lesson_view_history_dict.get(lesson['id'])
            if history:
                lesson['status'] = "Просмотрено" if history.status else "Не просмотрено"
                lesson['duration'] = history.duration
            else:
                lesson['status'] = "Не просмотрено"
                lesson['duration'] = None

        return Response(serialized_lessons, status=status.HTTP_200_OK)


class ProductLessonListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        user = request.user

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        if not ProductAccess.objects.filter(user=user, product=product).exists():
            return Response({"message": "You don't have access to this product"}, status=status.HTTP_403_FORBIDDEN)

        lesson_list = Lesson.objects.filter(products=product)

        serialized_lessons = LessonSerializer(lesson_list, many=True).data

        lesson_view_history = LessonViewHistory.objects.filter(lesson__in=lesson_list, user=user).order_by('lesson', '-duration')
        lesson_view_history_dict = {history.lesson_id: history for history in lesson_view_history}

        for lesson in serialized_lessons:
            history = lesson_view_history_dict.get(lesson['id'])
            if history:
                lesson['status'] = "Просмотрено" if history.status else "Не просмотрено"
                lesson['duration'] = history.duration
                lesson['last_change'] = history.last_change
            else:
                lesson['status'] = "Не просмотрено"
                lesson['duration'] = None
                lesson['last_change'] = None


        return Response(serialized_lessons, status=status.HTTP_200_OK)

class ProductStatisticsAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        products = Product.objects.all()

        product_statistics = products.annotate(
            total_viewed_lessons=Count('lesson', filter=Q(lesson__lessonviewhistory__status=True)),
            total_time_spent=Coalesce(Sum('lesson__lessonviewhistory__duration'), 0),
            total_students=Count('productaccess')
        )

        total_users = User.objects.count()
        product_statistics = product_statistics.annotate(
            acquisition_percent=ExpressionWrapper(
                F('total_students') * 100 / total_users,
                output_field=FloatField()
            )
        )

        serialized_product_statistics = [{
            'name': product.name,
            'total_viewed_lessons': product.total_viewed_lessons,
            'total_time_spent': product.total_time_spent,
            'total_students': product.total_students,
            'acquisition_percent': product.acquisition_percent
        } for product in product_statistics]

        return Response(serialized_product_statistics)
