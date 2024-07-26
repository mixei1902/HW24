from django.contrib.auth.models import AbstractUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractUser):
    """
    Модель пользователя, наследующая от AbstractUser.
    """

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """
    Модель для представления платежей.
    """

    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.payment_date}"


class CoursePurchase(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите курс",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        help_text="Укажите сумму оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии Stripe",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )

    class Meta:
        verbose_name = "Покупка курса"
        verbose_name_plural = "Покупки курсов"

    def __str__(self):
        return f"Покупка курса {self.course.title} пользователем {self.user.email} на сумму {self.amount} USD"
