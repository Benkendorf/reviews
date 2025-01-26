from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user.permissions import IsAdminRole
from user.serializers import SignUpSerializer, TokenSerializer, UserSerializer, MeSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all().order_by('id')

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {'username': 'Пользователь с таким username уже существует.'}
            )
        user = serializer.save()

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            if User.objects.filter(username=username).exclude(email=email).exists():
                return Response(
                    {'email': 'Пользователь с таким Никнеймом уже существует.'},
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
    serializer_class = MeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ('get', 'patch')
    pagination_class = None

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        user = request.user
        serializer = MeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
