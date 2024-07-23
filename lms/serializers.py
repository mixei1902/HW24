from rest_framework.fields import SerializerMethodField, URLField
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson
from .validators import validate_forbidden_words


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """
    video_url = URLField(validators=[validate_forbidden_words])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course.
    """
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    """
    Сериализатор для детализированного представления модели Course.
    """
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count', 'lessons']
