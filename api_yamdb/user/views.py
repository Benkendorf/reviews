from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.permissions import IsAdminRole
from user.serializers import SignUpSerializer, TokenSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = LimitOffsetPagination

def perform_create(self, serializer):
        serializer.save()


class SignUpViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exclude(username=username).exists():
                return Response(
                    {'email': 'Пользователь с таким email уже существует.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user, created = User.objects.get_or_create(username=username, email=email)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Confirmation code for accessing the YaMDB API',
                message=f'Код подтверждения для пользователя {username}: {confirmation_code}',
                from_email='yamdb@yamdb.ru',
                recipient_list=[email],
                fail_silently=False,
            )

            return Response(
                {'username': username, 'email': email},
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {'error': f'Пользователь с ником {username} не найден'},
                    status=status.HTTP_404_NOT_FOUND
                )
            if not default_token_generator.check_token(user, confirmation_code):
                return Response(
                    {'error': 'Неверный confirmation_code'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            tokens = user.tokens()

            return Response({'token': tokens['access']}, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class MeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def partial_update(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
