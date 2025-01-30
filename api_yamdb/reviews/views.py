from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .permissions import (OwnerOrModerOrAdminOrSuperuserOrReadOnly,
                          AdminOrSuperuserOrReadOnly)
from .serializers import (CategorySerializer,
                          CommentCreateSerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          ReviewCreateSerializer,
                          TitleSerializer,
                          TitleCreateSerializer,
                          TitleUpdateSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleCreateSerializer
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return TitleSerializer
        elif self.action == 'partial_update':
            return TitleUpdateSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrModerOrAdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return ReviewSerializer
        return ReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModerOrAdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return CommentSerializer
        return CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
