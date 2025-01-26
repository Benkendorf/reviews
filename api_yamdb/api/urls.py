from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import (CategoryViewSet,
                           GenreViewSet,
                           TitleViewSet,
                           ReviewViewSet,
                           CommentViewSet)
from user.views import SignUpViewSet, TokenViewSet, UserViewSet, MeViewSet

router_v1 = DefaultRouter()
router_v1.register(r'auth/signup', SignUpViewSet, basename='signup')
router_v1.register(r'auth/token', TokenViewSet, basename='token')
router_v1.register(r'users/me', MeViewSet, basename='me')
router_v1.register(r'users', UserViewSet, basename='users')

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
    path('v1/', include(router_v1.urls)),
]
