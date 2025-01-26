from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Пользователь с именем me запрещен.')
        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return email

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('id', 'role',)


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )

    def validate_username(self, username):
        if username == 'me':
            raise ValidationError('Пользователь с именем me запрещен.')
        return username

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=False
    )
    email = serializers.EmailField(
        max_length=254,
        required=False
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ('id', 'role',)
