from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.constants import MAX_SCORE, MIN_SCORE
from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('slug', 'name')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('slug', 'name')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        read_only=True,
        default=0
    )

    class Meta:
        fields = '__all__'
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
    year = serializers.IntegerField()

    def to_representation(self, instance):
        return TitleSerializer(instance).data

    class Meta:
        fields = '__all__'
        model = Title

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
        if self.context['request'].method != 'PATCH':
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


class ReviewCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    score = serializers.IntegerField()

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate_score(self, value):
        if not (MIN_SCORE < value <= MAX_SCORE):
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}!'
            )
        return value

    def validate(self, data):
        title_id = self.context.get('request'
                                    ).parser_context.get('kwargs'
                                                         ).get('title_id')

        title = get_object_or_404(
            Title,
            id=title_id
        )
        if self.context['request'].method == 'POST' and Review.objects.filter(
            title=title,
            author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв к этому произведению!'
            )
        return data


class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
