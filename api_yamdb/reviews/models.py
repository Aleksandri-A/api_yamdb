from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

LETTERS_LIMIT = 15


class Category(models.Model):
    """Модель категорий."""

    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров."""

    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        db_index=True
    )
    year = models.IntegerField(
        verbose_name='Год выпуска',
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        related_name='titles',
        verbose_name='Жанры',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Модель для связи многие-ко-многим для произведений и жанров."""

    title = models.ForeignKey(
        Title,
        null=True,
        on_delete=models.SET_NULL,
        related_name='title'
    )
    genre = models.ForeignKey(
        Genre,
        null=True,
        on_delete=models.SET_NULL,
        related_name='genre'
    )

    class Meta:
        unique_together = ('title', 'genre')
        ordering = ('title',)

    def __str__(self):
        return f'{self.title} - {self.genre}'


class Review(models.Model):
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
        db_index=True,
        null=False
    )
    text = models.TextField('Содержание отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        db_index=True,
        null=False
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        null=False,
        validators=(
            MinValueValidator(1, 'Минимум 1',),
            MaxValueValidator(10, 'Максимум 10',)
        ),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_title_author'
            ),
        )

    def __str__(self):
        return self.text[:LETTERS_LIMIT]


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Название',
        db_index=True,
        null=False
    )
    text = models.TextField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
        db_index=True,
        null=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:LETTERS_LIMIT]
