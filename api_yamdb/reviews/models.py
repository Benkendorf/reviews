from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

from .validators import validate_year_not_future
from api.constants import (CHAR_FIELD_MAX_LENGTH,
                           TEXT_CUTOFF_LENGTH,
                           MIN_SCORE_VALUE,
                           MAX_SCORE_VALUE)

User = get_user_model()


class DefaultModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[TEXT_CUTOFF_LENGTH]


class Category(DefaultModel):
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta(DefaultModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(DefaultModel):
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta(DefaultModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(DefaultModel):
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название'
    )
    year = models.SmallIntegerField(
        verbose_name='Год выпуска',
        validators=[
            validate_year_not_future
        ]
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание'
    )

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name='Категория'
    )

    class Meta(DefaultModel.Meta):
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']
        default_related_name = 'titles'


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.DO_NOTHING,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )


class DefaultReviewCommentModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[TEXT_CUTOFF_LENGTH]


class Review(DefaultReviewCommentModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE_VALUE),
            MaxValueValidator(MAX_SCORE_VALUE)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta(DefaultReviewCommentModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'

        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comment(DefaultReviewCommentModel):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta(DefaultReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
