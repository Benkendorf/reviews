import re

from django.core.exceptions import ValidationError

from api.constants import PATTERN_NAME, PATTERN_ME


def validate_me(username):
    if username == PATTERN_ME:
        raise ValidationError('Пользователь с именем me запрещен.')
    return username


def validate_regex(username):
    if not re.match(PATTERN_NAME, username):
        raise ValidationError(
            'Имя пользователя должно соответствовать шаблону ^[\\w.@+-]+\\Z'
        )
    return username
