from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name='Никнэйм'
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        unique=False
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='Фамилия'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def __str__(self):
        return self.username
