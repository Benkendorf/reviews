from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from api.constants import (EMAIL_SENDERS_YAMDB,
                           MAX_LENGTH_NAME,
                           MAX_LENGTH_EMAIL,
                           PATTERN_NAME)
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


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=PATTERN_NAME,
        max_length=MAX_LENGTH_NAME,
        required=True,
        validators=[validate_me, validate_regex]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, validate_data):
        username = validate_data['username']
        email = validate_data['email']
        if User.objects.filter(
            email=email
        ).exclude(username=username).exists():
            raise ValidationError({'email': 'email уже существует.'})
        if User.objects.filter(
            username=username
        ).exclude(email=email).exists():
            raise ValidationError({'username': 'username уже существует.'})
        return validate_data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        confirm_code = default_token_generator.make_token(user)

        send_mail(
            subject="Код подтверждения для YaMDB",
            message=f"Ваш код подтверждения: {confirm_code}",
            from_email="noreply@yamdb.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=PATTERN_NAME,
        max_length=MAX_LENGTH_NAME,
        required=True
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, validate_data):
        username = validate_data['username']
        confirm_code = validate_data['confirmation_code']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound({'error': 'Пользователь не найден'})
        if not default_token_generator.check_token(user, confirm_code):
            raise ValidationError({'error': 'Неверный confirmation_code'})
        validate_data['user'] = user
        return validate_data
