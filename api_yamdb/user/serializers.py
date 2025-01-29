from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotFound

from api.constants import MAX_LENGTH_NAME, PATTERN_NAME, EMAIL_SENDERS_YAMDB
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
            raise ValidationError(
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

    def validate(self, validate_data):
        user = validate_data['username']
        email = validate_data['email']

        if User.objects.filter(email=email).exclude(username=user).exists():
            raise ValidationError(
                {'email': 'Пользователь с таким email уже существует.'}
            )
        if User.objects.filter(username=user).exclude(email=email).exists():
            raise ValidationError(
                {'username': 'Пользователь с таким никнеймом уже существует.'}
            )
        return validate_data

    def create(self, validate_data):
        user, created = User.objects.get_or_create(
            username=validate_data['username'],
            email=validate_data['email']
        )
        if created:
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Confirmation code for accessing the YaMDB API',
                message=f'Код подтверждения для пользователя {user.username}: {confirmation_code}',
                from_email=EMAIL_SENDERS_YAMDB,
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

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, validate_data):
        username = validate_data['username']
        confirmation_code = validate_data['confirmation_code']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound({'error': 'Пользователь не найден'})
        if not default_token_generator.check_token(user, confirmation_code):
            raise ValidationError({'error': 'Неверный confirmation_code'})
        validate_data['user'] = user
        return validate_data
