from django.conf import settings
from django.db import models

from users.models import User


class Course(models.Model):
    """
    Модель для представления курса.
    """
    title = models.CharField(max_length=255, verbose_name="Название курса", help_text="Укажите название курса")
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True, verbose_name="Аватар",
                                help_text="Загрузите аватар")
    description = models.TextField(verbose_name="Описание курса", help_text="Опишите содержание курса")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses', on_delete=models.CASCADE, verbose_name="Владелец", help_text="Владелец курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """
    Модель для представления урока.
    """
    title = models.CharField(max_length=255, verbose_name="Название урока", help_text="Укажите название урока")
    description = models.TextField(verbose_name="Описание", help_text="Опишите содержание урока")
    preview = models.ImageField(upload_to='lesson_previews/', blank=True,
                                null=True, verbose_name="Превью", help_text="Загрузите изображение")
    video_url = models.URLField(verbose_name="Ссылка на видео", help_text="Заполните ссылку на видео", blank=True,
                                null=True)
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE, verbose_name="Курс",
                               help_text="Выберите курс")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lessons', on_delete=models.CASCADE,
                              verbose_name="Владелец", help_text="Владелец урока")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
