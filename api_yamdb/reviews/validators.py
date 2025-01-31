from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year_not_future(value):
    if value > datetime.now().year:
        raise ValidationError(
            'Нельзя добавить произведение из будущего!',
        )
