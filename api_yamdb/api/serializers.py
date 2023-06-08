import datetime as dt
import re

from django.db import models
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор title для запросов 'GET'."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(
        read_only=True 
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')
        model = Title


class TitleUnsaveSerializer(serializers.ModelSerializer):
    """Сериализатор title для запросов 'POST', 'DELETE'."""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    # genre = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    def validate(self, attrs):
        if 'category' not in attrs or attrs['category'] is None:
            raise serializers.ValidationError('Укажите категорию')
        if 'genre' not in attrs or not attrs['genre']:
            raise serializers.ValidationError('Укажите жанр')
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        genre_data = data.pop('genre')        
        genres = [{
            "name": Genre.objects.get(slug=genre).name,
            "slug": genre
        } for genre in genre_data]
        data['genre'] = genres
        category_data = data.pop('category')
        _category = {
            "name": Category.objects.get(slug=category_data).name,
            "slug": Category.objects.get(slug=category_data).slug    
        }
        data['category'] = _category
        data['rating'] = 0
        return data


class TitlePatchSerializer(serializers.ModelSerializer):
    """Сериализатор title для запросов 'PATCH'."""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    # genre = serializers.SerializerMethodField()
    # category = serializers.SerializerMethodField()
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',
                  'rating')

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value

    # def validate(self, attrs):
    #     if 'category' not in attrs or attrs['category'] is None:
    #         raise serializers.ValidationError('Укажите категорию')
    #     if 'genre' not in attrs or not attrs['genre']:
    #         raise serializers.ValidationError('Укажите жанр')
    #     return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        genre_data = data.pop('genre')        
        genres = [{
            "name": Genre.objects.get(slug=genre).name,
            "slug": genre
        } for genre in genre_data]
        data['genre'] = genres
        category_data = data.pop('category')
        _category = {
            "name": Category.objects.get(slug=category_data).name,
            "slug": Category.objects.get(slug=category_data).slug    
        }
        data['category'] = _category
        # data['rating'] = 0
        return data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
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
                'Одно произведение - один отзыв!.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев."""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review', 'author')
