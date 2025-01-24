from datetime import datetime

from rest_framework import serializers

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    description = serializers.CharField(
        required=False
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        if value > datetime.now().year():
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
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get(
                **genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
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
