from rest_framework.exceptions import ValidationError


def validate_forbidden_words(value):
    """
    Валидатор для проверки наличия запрещенных слов в ссылке.
    Разрешает только ссылки, которые не содержат запрещенные слова.
    """
    forbidden_words = [
        "rutube.ru",
        "vkvideo.ru",
    ]

    for word in forbidden_words:
        if word in value:
            raise ValidationError(f"Ссылки на {word} запрещены.")

    if not value.startswith("https://www.youtube.com") and not value.startswith(
        "https://youtu.be"
    ):
        raise ValidationError("Допустимы только ссылки на youtube.com.")
