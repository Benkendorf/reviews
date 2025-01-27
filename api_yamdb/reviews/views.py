from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import render

from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Category, Comment, Genre, Review, Title
from .permissions import (OwnerOrModerOrAdminOrSuperuserOrReadOnly,
                          AdminOrSuperuserOrReadOnly,
                          AdminOrSuperuser)
from .serializers import (CategorySerializer,
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
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleCreateSerializer
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug',)

    #search_fields = ('genre__slug',)

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
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModerOrAdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
