from django.shortcuts import render

from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Category, Comment, Genre, Review, Title
from .permissions import (OwnerOrModerOrAdminOrSuperuserOrReadOnly,
                          AdminOrSuperuserOrReadOnly,
                          AdminOrSuperuser)
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleSerializer)


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
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    permission_classes = (AdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('id')
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrModerOrAdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('id')
    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModerOrAdminOrSuperuserOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
