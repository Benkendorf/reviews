from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

urlpatterns = [
    re_path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('user.urls')),
    path('v1/users/', include('user.urls')),
]
