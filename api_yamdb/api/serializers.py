import datetime as dt

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title, User
from .validators import username_validator, validate_email, validate_username


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = 'name', 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериализатор произведений для чтения."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'rating', 'description', 'genre',
                  'category')
        read_only_fields = ('id', 'name', 'year',
                            'description', 'genre',
                            'category', 'rating')


class TitleSerializer(TitleViewSerializer):
    """Сериализатор произведений для записи."""
    rating = serializers.IntegerField(read_only=True)

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=False,
        required=True
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год произведения!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate_score(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError(
                'Проверьте, что score от 0 до 10!'
            )
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id'])
            author = self.context['request'].user
            if author.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили свой отзыв.'
                )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации новых пользователей."""

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])

    class Meta:
        model = User
        fields = (
            'email',
            'username'
        )


class AdminCreationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для администратора, который может создавать пользователей.
    """

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя."""

    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email])
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username, username_validator])
    first_name = serializers.CharField(
        max_length=150,
        allow_blank=True)
    last_name = serializers.CharField(
        max_length=150,
        allow_blank=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio'
        )


class TokenSerializer(serializers.ModelSerializer):
    """
    Сериализатор для токена с учетом проверки confirmation_code.
    """

    username = serializers.CharField(
        max_length=150,
        allow_blank=False)
    confirmation_code = serializers.CharField(allow_blank=False,)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, value):
        user = get_object_or_404(User, username=value['username'])
        confirmation_code = value['confirmation_code']
        if default_token_generator.check_token(
                user, confirmation_code) is False:
            raise ValidationError('Неверный код подтверждения')
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев.
    """

    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('review',)
