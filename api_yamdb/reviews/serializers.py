from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )

    class Meta:
        fields = ('slug', 'name')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        validators=[UniqueValidator(queryset=Genre.objects.all())]
    )

    class Meta:
        fields = ('slug', 'name')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False,
    )
    category = CategorySerializer()
    description = serializers.CharField(
        required=False
    )

    class Meta:
        fields = ('id', 'name', 'year', 'genre', 'category', 'description')
        model = Title

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Название не может быть длиннее 256 символов!'
            )
        return value

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего!'
            )
        return value

    def validate(self, data):
        if data['category'] not in Category.objects.all():
            raise serializers.ValidationError(
                'Нельзя добавить произведение несуществующей категории!'
            )

        for genre in data['genre']:
            if genre not in Genre.objects.all():
                raise serializers.ValidationError(
                    'Нельзя добавить произведение несуществующего жанра!'
                )

        return data

    def create(self, validated_data):
        print('CREATE')
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            """
            current_genre = get_object_or_404(
                Genre,
                slug=genre
            )
            """
            GenreTitle.objects.create(
                genre=genre, title=title)
        return title


class ReviewSerializer(serializers.ModelSerializer):
    title = TitleSerializer()
    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if not (1 < value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value


class CommentSerializer(serializers.ModelSerializer):
    title = TitleSerializer()
    review = ReviewSerializer()
    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Comment
