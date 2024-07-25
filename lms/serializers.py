from rest_framework.fields import SerializerMethodField, URLField
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson, Subscription
from .validators import validate_forbidden_words


class LessonSerializer(ModelSerializer):
    """
    Сериализатор для модели Lesson.
    """

    video_url = URLField(validators=[validate_forbidden_words])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course.
    """

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    Сериализатор для детализированного представления модели Course.
    """

    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """
        Возвращает True, если пользователь подписан на курс
        """
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lesson_count", "lessons", 'is_subscribed']


class SubscriptionSerializer(ModelSerializer):
    """
    Сериализатор для модели Subscription.
    """

    class Meta:
        model = Subscription
        fields = ["user", "course"]
