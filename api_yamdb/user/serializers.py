from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.constants import MAX_LENGTH_NAME, PATTERN_NAME
from user.validators import validate_me, validate_regex

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default=User.USER
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return email


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=PATTERN_NAME,
        max_length=MAX_LENGTH_NAME,
        required=True,
        validators=[validate_me, validate_regex]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, obj):
        user = obj['username']
        email = obj['email']

        if User.objects.filter(email=email).exclude(username=user).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким email уже существует.'}
            )
        if User.objects.filter(username=user).exclude(email=email).exists():
            raise serializers.ValidationError(
                {'username': 'Пользователь с таким никнеймом уже существует.'}
            )
        return obj


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=PATTERN_NAME,
        max_length=MAX_LENGTH_NAME,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=PATTERN_NAME,
        max_length=MAX_LENGTH_NAME,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
