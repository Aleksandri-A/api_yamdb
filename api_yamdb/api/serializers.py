from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

import datetime as dt

from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор title"""
    genre = SlugRelatedField(slug_field='slug', read_only=True)
    category = SlugRelatedField(slug_field='slug', read_only=True)
    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value >= current_year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор genre"""
    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор category"""
    class Meta:
        fields = '__all__'
        model = Category
