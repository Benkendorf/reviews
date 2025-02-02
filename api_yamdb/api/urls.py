from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import (CategoryViewSet,
                           GenreViewSet,
                           TitleViewSet,
                           ReviewViewSet,
                           CommentViewSet)
from user.views import SignUp, Token, UserViewSet

router_v1 = DefaultRouter()
# Маршруты приложения user
router_v1.register('users', UserViewSet, basename='users')
auth_urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('token/', Token.as_view(), name='token')
]
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
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include((auth_urlpatterns, 'auth'), namespace='auth'))
]
