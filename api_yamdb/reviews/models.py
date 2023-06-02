from django.db import models


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
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
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
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
        # blank=True,
        # null=True,
        # on_delete=models.SET_NULL,
        # related_name='titles',
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
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('title', 'genre')

    def __str__(self):
        return f'{self.title} - {self.genre}'
