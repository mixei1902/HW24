from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonDestroyAPIView, LessonUpdateAPIView, LessonRetrieveAPIView
from lms.views import LessonCreateAPIView, LessonListAPIView

app_name = LmsConfig.name

router = SimpleRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path("lms/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lms/<int:pk>", LessonRetrieveAPIView.as_view(), name="lessons_retrieve"),
    path("lms/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lms/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path("lms/<int:pl>,/update/", LessonUpdateAPIView.as_view(), name="lessons_update"),

]
urlpatterns += router.urls
