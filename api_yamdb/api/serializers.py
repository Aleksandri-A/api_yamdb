import datetime as dt
import re
import statistics as st

from rest_framework import serializers

from reviews.models import Category, Genre, Title


class Review(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор genre."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre

    def validate_slug(self, value):
        """Валидация имени слага."""
        regex = r'^[-a-zA-Z0-9_]+$'
        if not re.match(regex, value):
            raise serializers.ValidationError('Неверное имя slug')
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор category."""
    class Meta:
        fields = ('name', 'slug')
        model = Category

    def validate_slug(self, value):
        """Валидация имени слага."""
        regex = r'^[-a-zA-Z0-9_]+$'
        if not re.match(regex, value):
            raise serializers.ValidationError('Неверное имя slug')
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор title для запросов 'GET'."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title
    
    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        rev = Review.objects.filter(title=obj).aggregate(
            rating=st.mean('score')
        )
        return rev['rating']


class TitleUnsaveSerializer(serializers.ModelSerializer):
    """Сериализатор title для запросов 'POST', 'PATCH', 'DELETE'."""
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value