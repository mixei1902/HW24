from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from .models import Subscription

@shared_task
def send_course_update_emails(course_id, update_message):
    """
    Отправляет письма всем подписчикам курса о его обновлении.
    """
    subscriptions = Subscription.objects.filter(course_id=course_id)
    for subscription in subscriptions:
        send_mail(
            'Обновление курса',
            update_message,
            EMAIL_HOST_USER,
            [subscription.user.email],
            fail_silently=False,
        )
