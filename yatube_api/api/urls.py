from rest_framework import routers
from django.urls import path, include

from .views import (
    GroupViewSet,
    PostViewSet,
    CommentViewSet,
    FollowViewSet
)

router = routers.DefaultRouter()
router.register(r'v1/groups', GroupViewSet)
router.register(r'v1/posts', PostViewSet)
router.register(r'v1/comments', CommentViewSet)
router.register(r'v1/follow', FollowViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('v1/', include('djoser.urls')),  # Работа с пользователями
    path('v1/', include('djoser.urls.jwt')),  # Работа с токенами
]
