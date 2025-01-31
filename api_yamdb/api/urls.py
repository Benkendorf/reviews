from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import (CategoryViewSet,
                           GenreViewSet,
                           TitleViewSet,
                           ReviewViewSet,
                           CommentViewSet)
from user.views import SignUpViewSet, TokenViewSet, UserViewSet

router_v1 = DefaultRouter()
# Маршруты приложения user
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', SignUpViewSet, basename='signup')
router_v1.register('auth/token', TokenViewSet, basename='token')
# Маршруты приложения reviews
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls))
]
