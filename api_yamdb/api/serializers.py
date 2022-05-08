from django.db.models import Avg
from rest_framework import serializers
from reviews.models import (Category, Comments, Genre, Review, Title,
                            current_year)

from api_yamdb.settings import START_YEAR


class ReviewSerializer(serializers.ModelSerializer):
    '''Сериалайзер отзывов.'''
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title', 'author')

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise serializers.ValidationError(
                'Нельзя оставить два отзыва на одно произведение.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериалайзер комментариев.'''
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review', 'author')


class CategorySerializer(serializers.ModelSerializer):
    '''Сериалайзер категорий.'''
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    '''Сериалайзер жанров.'''
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    '''Сериалайзер произведений.'''
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=False,
        required=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, year):
        '''Валидация поля year.'''
        if not (START_YEAR <= year <= current_year()):
            raise serializers.ValidationError('Год не подходит')
        return year


class TitleViewSerializer(serializers.ModelSerializer):
    '''Сериалайзер произведений.'''
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=True,)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        '''Подсчет рейтинга произведения.'''
        if obj.reviews.count() == 0:
            return None
        r = Review.objects.filter(title=obj).aggregate(rating=Avg('score'))
        return r['rating']
