from datetime import datetime

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def validate(self, data):
        if data['year'] > datetime.now().year():
            raise serializers.ValidationError(
                'Нельзя добавить произведение из будущего!'
            )
        return data
