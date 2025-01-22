from datetime import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


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

    class Meta:
        fields = '__all__'
        model = Title

    def validate(self, data):
        if data['year'] > datetime.now().year():
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего!'
            )
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
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Title.objects.create(**validated_data)
            for genre in genres:
                current_genre, status = Genre.objects.get(
                    **genre)
                GenreTitle.objects.create(
                    genre=current_genre, title=title)
            return title
