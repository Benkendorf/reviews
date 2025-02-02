from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_year_not_future
from api.constants import (CHAR_FIELD_MAX_LENGTH,
                           TEXT_CUTOFF_LENGTH,
                           MIN_SCORE,
                           MAX_SCORE)

User = get_user_model()


class AbstractNameSlugModel(models.Model):
    name = models.CharField(
        max_length=CHAR_FIELD_MAX_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name[TEXT_CUTOFF_LENGTH]


class Category(AbstractNameSlugModel):
    class Meta(AbstractNameSlugModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractNameSlugModel):
    class Meta(AbstractNameSlugModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
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

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']
        default_related_name = 'titles'

    def __str__(self):
        return self.name[TEXT_CUTOFF_LENGTH]


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

    def __str__(self):
        return f'Жанр: {self.genre}, произведение: {self.title}'


class DefaultReviewCommentModel(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

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

    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)
        ],
        verbose_name='Оценка'
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
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta(DefaultReviewCommentModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
