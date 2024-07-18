from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, CanEditLessonOrCourse
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(ModelViewSet):
    """
    ViewSet для модели Course.
    """
    queryset = Course.objects.all()

    def get_serializer_class(self):
        """
        Возвращает сериализатор в зависимости от действия.
        """
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """
        Определяет права доступа в зависимости от действия.
        """
        if self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsModerator | CanEditLessonOrCourse]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated, IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
       Представление для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

class LessonListAPIView(ListAPIView):
    """
    Представление для отображения списка уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

class LessonUpdateAPIView(UpdateAPIView):
    """
    Представление для обновления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | CanEditLessonOrCourse]

class LessonDestroyAPIView(DestroyAPIView):
    """
    Представление для удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Представление для получения детальной информации об уроке.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated,]
