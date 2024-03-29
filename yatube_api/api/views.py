from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from posts.models import (
    Group,
    Post,
    Comment,
    Follow
)
from .serializers import (
    GroupSerializer,
    PostSerializer,
    CommentSerializer,
    FollowSerializer
)

from .permissions import AuthorOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            post=self.kwargs.get("post_id")
        )
        return queryset

    def perform_create(self, serializer):
        post_id = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )

        serializer.save(
            author=self.request.user,
            post=post_id
        )


class CreateListFollowViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    pass


class LightFollowViewSet(CreateListFollowViewSet):
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):

        queryset = Follow.objects.filter(
            user=self.request.user
        )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
