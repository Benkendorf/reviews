from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Review, Title
from .permissions import (OwnerOrModerOrAdminOrSuperuserOrReadOnly,
                          AdminOrSuperuserOrReadOnly)
from .serializers import (CategorySerializer,
                          CommentCreateSerializer,
                          GenreSerializer,
                          ReviewCreateSerializer,
                          TitleSerializer,
                          TitleCreateSerializer)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrSuperuserOrReadOnly,)


class DefaulPaginationModelViewset(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer


class TitleViewSet(DefaulPaginationModelViewset):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleCreateSerializer
    permission_classes = (AdminOrSuperuserOrReadOnly,)

    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'destroy'):
            return TitleSerializer
        return TitleCreateSerializer


class ReviewViewSet(DefaulPaginationModelViewset):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    serializer_class = ReviewCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          OwnerOrModerOrAdminOrSuperuserOrReadOnly)

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            title=self.get_title(),
            author=self.request.user
        )


class CommentViewSet(DefaulPaginationModelViewset):
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          OwnerOrModerOrAdminOrSuperuserOrReadOnly)

    def get_review(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs['title_id']
        )
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title=title
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(),
            author=self.request.user
        )
