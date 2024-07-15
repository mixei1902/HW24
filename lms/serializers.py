from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count']


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
