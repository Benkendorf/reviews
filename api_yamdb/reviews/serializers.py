from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.serializers import UserSerializer

User = get_user_model()


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
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    description = serializers.CharField(
        required=False
    )

    class Meta:
        fields = ('id', 'name', 'year', 'genre',
                  'rating', 'category', 'description')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
    )
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

        if 'genre' not in data:
            raise serializers.ValidationError(
                'Нельзя добавить произведение без жанра!'
            )

        for genre in data['genre']:
            if genre not in Genre.objects.all():
                raise serializers.ValidationError(
                    'Нельзя добавить произведение несуществующего жанра!'
                )

        return data

    def create(self, validated_data):
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


class TitleUpdateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
    )
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

    def update(self, instance, validated_data):
        if 'genre' in validated_data:
            genres = validated_data.pop('genre')
            for genre in genres:
                current_genre, genre_status = Genre.objects.get_or_create(
                    **genre
                )
                GenreTitle.objects.get_or_create(
                    genre=current_genre, title=instance)

        if 'name' in validated_data:
            instance.name = validated_data['name']
        if 'year' in validated_data:
            instance.year = validated_data['year']
        if 'description' in validated_data:
            instance.description = validated_data['description']
        if 'category' in validated_data:
            instance.category = validated_data['category']
        instance.save()
        return instance


class ReviewCreateSerializer(serializers.ModelSerializer):

    title = serializers.PrimaryKeyRelatedField(
        queryset=Title.objects.all(),
        required=False
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate_score(self, value):
        if not (1 < value <= 10):
            raise serializers.ValidationError('Оценка должна быть от 1 до 10!')
        return value

    def create(self, validated_data):
        title_id = self.context.get('request'
                                    ).parser_context.get('kwargs'
                                                         ).get('title_id')

        title = get_object_or_404(
            Title,
            id=title_id
        )

        review = Review.objects.create(
            title=title,
            author=self.context['request'].user,
            text=validated_data['text'],
            score=validated_data['score']
        )
        return review


class ReviewSerializer(serializers.ModelSerializer):
    title = TitleCreateSerializer()
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    title = TitleCreateSerializer()
    review = ReviewSerializer()
    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Comment
