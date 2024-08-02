from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, CanEditLessonOrCourse, IsOwner
from .models import Course, Lesson, Subscription
from .pagination import CustomPagination
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from .tasks import send_course_update_emails

class CourseViewSet(ModelViewSet):
    """
    ViewSet для модели Course.
    """

    queryset = Course.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        """
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """
        Определяет права доступа в зависимости от действия.
        """
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [
                IsAuthenticated,
                IsModerator | CanEditLessonOrCourse,
            ]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Привязывает создаваемый курс к текущему пользователю.
        """
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """
        Обновляет курс и отправляет письма подписчикам.
        """
        course = serializer.save()
        update_message = f"Курс '{course.title}' был обновлен. Проверьте новые материалы."
        send_course_update_emails.delay(course.id, update_message)


class LessonCreateAPIView(CreateAPIView):
    """
    Представление для создания урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """
        Привязывает создаваемый курс к текущему пользователю.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """
    Представление для отображения списка уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonUpdateAPIView(UpdateAPIView):
    """
    Представление для обновления урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, CanEditLessonOrCourse]


class LessonDestroyAPIView(DestroyAPIView):
    """
    Представление для удаления урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Представление для получения детальной информации об уроке.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class SubscriptionAPIView(APIView):
    """
    Представление для управления подписками пользователя на курсы.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запросы на добавление или удаление подписки пользователя на курс.
        Если подписка существует, удаляет ее. Если не существует, создает новую подписку.
        """
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=user, course=course
        )

        if created:
            message = "Подписка добавлена"
        else:
            subscription.delete()
            message = "Подписка удалена"

        return Response({"message": message})
