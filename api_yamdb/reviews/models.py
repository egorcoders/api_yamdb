import datetime as dt

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


def current_year():
    return dt.datetime.today().year


class Title(models.Model):
    """Модель произведений."""
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
    )
    name = models.CharField(max_length=200)
    year = models.IntegerField(default=current_year,)
    description = models.TextField(max_length=200, null=True,)

    def __str__(self) -> str:
        return self.category[:10]


class Category(models.Model):
    """Модель категорий."""
    name = models.CharField(max_length=200,)
    slug = models.SlugField(
        max_length=100, unique=True,
    )

    def __str__(self) -> str:
        return self.slug[:10]


class Genre(models.Model):
    """Модель жанров."""
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=100, unique=True,)

    def __str__(self) -> str:
        return self.slug[:10]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title},{self.genre}'


class Review(models.Model):
    """Модель отзывов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique follow',)
        ]


class Comments(models.Model):
    """Модель комментариев."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
