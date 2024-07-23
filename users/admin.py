from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели User.
    """

    list_display = ["pk", "email", "is_active", "is_staff", "is_superuser"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Payment.
    """

    list_display = ["pk", "user", "amount", "payment_date", "payment_method"]
