from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views import SignUpViewSet, TokenViewSet, MeViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'signup', SignUpViewSet, basename='signup')
router_v1.register(r'token', TokenViewSet, basename='token')
router_v1.register(r'', UserViewSet, basename='users')


urlpatterns = [
    *router_v1.urls,
    path('me/', MeViewSet.as_view({'patch': 'partial_update'}), name='me')
]
