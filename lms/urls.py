from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonDestroyAPIView, LessonUpdateAPIView, LessonRetrieveAPIView
from lms.views import LessonCreateAPIView, LessonListAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path("les/", LessonListAPIView.as_view(), name="lessons_list"),
    path("les/<int:pk>", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("les/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("les/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path("les/<int:pl>,/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),

]
urlpatterns += router.urls
