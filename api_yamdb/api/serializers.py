from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title, Genre, Category


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор title"""
    class Meta:
        fields = '__all__'
        model = Title


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
