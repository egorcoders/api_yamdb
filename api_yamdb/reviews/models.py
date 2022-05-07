import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.forms import ValidationError
from users.models import User


def current_year():
    return dt.datetime.today().year


def validate_year(year):
    '''Валидация поля year.'''
    current_year = dt.datetime.today().year
    if not (0 <= year <= current_year):
        raise ValidationError('Год не подходит')


class Title(models.Model):
    '''Модель произведений.'''
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_index=True,
    )
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
        db_index=True,
    )
    name = models.CharField(
        max_length=200,
        db_index=True,
    )
    year = models.IntegerField(
        db_index=True,
        validators=(validate_year,)
    )
    description = models.TextField(
        max_length=200,
        null=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.category[:10]


class Category(models.Model):
    '''Модель категорий.'''
    name = models.CharField(
        max_length=200,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug[:10]


class Genre(models.Model):
    '''Модель жанров.'''
    name = models.CharField(
        max_length=200,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self) -> str:
        return self.slug[:10]


class TitleGenre(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        ordering = ('title',)

    def __str__(self) -> str:
        return self.title, self.genre


class Review(models.Model):
    '''Модель отзывов.'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique author and title',
            )
        ]

    class Meta:
        ordering = ('author',)

    def __str__(self) -> str:
        return f'Ревью {self.author}'


class Comments(models.Model):
    '''Модель комментариев.'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления комментария',
        help_text='Укажите дату добавления комментария',
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self) -> str:
        return f'Комментарий {self.author}'
