from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ANONYMOUS = 'anonymous', 'Аноним'
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    username =  models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Никнэйм'
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name = 'Биография'
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

