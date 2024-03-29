import datetime as dt

from django.core.exceptions import ValidationError
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import Confirm, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели юзера."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class SignupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели регистрации."""

    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150)
    email = serializers.EmailField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
        max_length=254
    )

    def validate_username(self, value):
        """Функция валидации по логину."""

        username = value.lower()
        if username == 'me':
            raise ValidationError(
                'Username "me" не может быть создан, придумайте другое имя.'
            )
        return value

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения токена."""

    username = serializers.RegexField(
        required=True,
        regex=r'^[\w.@+-]+\Z',
        max_length=150
    )
    confirmation_code = serializers. CharField(
        max_length=400,
        required=True,
    )

    class Meta:
        model = Confirm
        fields = ('username', 'confirmation_code')


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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
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
        serializer = TitleSerializer(instance)
        return serializer.data


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

    def to_representation(self, instance):
        serializer = TitleSerializer(instance)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

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
        read_only_fields = ('review',)
