from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course"
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson",
            video_url="https://www.youtube.com/",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("lms:lessons_create")
        data = {
            "title": "Test Lesson",
            "description": "Test Lesson",
            "video_url": "https://www.youtube.com/",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Lesson.objects.all().count(),2)

    def test_lesson_list(self):
        """
        Тестирование списка уроков.
        """
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_lesson_retrieve(self):
        """
        Тестирование получения урока.
        """
        url = reverse("lms:lessons_retrieve", args=[self.lesson.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    #
    def test_lesson_update(self):
        """
        Тестирование обновления урока.
        """
        url = reverse("lms:lessons_update", args=(self.lesson.pk,))
        updated_data = {
            "title": "Updated Test Lesson",
            "description": "Updated Test Description",
            "video_url": "https://www.youtube.com/",
            "course": self.course.pk,
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Test Lesson")

    #
    def test_lesson_delete(self):
        """
        Тестирование удаления урока.
        """
        url = reverse("lms:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


#
#
class SubscriptionTestCase(APITestCase):

    def setUp(self):
        """
        Устанавливаем тестовые данные для тестов.
        """
        self.user = User.objects.create(email="user@sky.pro", password="password")
        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscribe_course(self):
        """
        Тестирование подписки на курс.
        """
        url = reverse("lms:subscription")
        response = self.client.post(url, {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertEqual(Subscription.objects.count(), 1)

    #
    def test_unsubscribe_course(self):
        """
        Тестирование отписки от курса.
        """
        # Подписываемся на курс
        self.client.post(reverse("lms:subscription"), {"course_id": self.course.id})
        # Отписываемся от курса
        response = self.client.post(
            reverse("lms:subscription"), {"course_id": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertEqual(Subscription.objects.count(), 0)
