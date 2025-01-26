from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.SmallIntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )

    rating = models.SmallIntegerField(
        default=None,
        null=True,
        blank=True
    )   # См. метод save()

    genre = models.ManyToManyField(Genre, through='GenreTitle')
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.DO_NOTHING
    )

    def save(self, *args, **kwargs):
        """При сохранении тайтла рассчитываем сред. балл из связанных ревью."""
        self.rating = Review.objects.filter(
            title=self
        ).aggregate(Avg('score'))['score__avg']

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE
    )

    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE
    )
    score = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        """При каждом сохранении/изменении ревью сохраняем связанный тайтл
        для перерасчета среднего рейтинга в тайтле.
        """

        super().save(*args, **kwargs)
        self.title.save()

    def __str__(self):
        return self.text


class Comment(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='comments',
        on_delete=models.CASCADE
    )

    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE
    )

    text = models.TextField()
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE
    )

    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.text
