from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.permissions import IsAdminRole
from user.serializers import (SignUpSerializer,
                              TokenSerializer,
                              UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all().order_by('username')

    @action(methods=['get', 'patch'],
            detail=False,
            url_name='me',
            permission_classes=[IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.serializer_class(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            serializer = self.serializer_class(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()


class SignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class Token(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = user.tokens()
        return Response({'token': tokens['access']}, status=status.HTTP_200_OK)
