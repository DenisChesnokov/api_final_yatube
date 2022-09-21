from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
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

from .permissions import AuthorOrReadOnly, ReadOnly, FollowPermission


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

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(
            post=self.kwargs.get("post_id")
        )
        return queryset

    def perform_create(self, serializer):
        print(self.kwargs.get('post_id'))
        post = get_object_or_404(
            Post,
            pk=self.kwargs.get('post_id')
        )

        serializer.save(
            author=self.request.user,
            post=post
        )

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (FollowPermission,)

    def get_queryset(self):

        queryset = Follow.objects.filter(
            user=self.request.user
        )

        following_name = self.request.query_params.get('search')
        print(following_name)

        if following_name is not None:
            queryset = queryset.filter(
                following__username=following_name
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )
