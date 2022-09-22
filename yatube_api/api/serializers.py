from rest_framework import serializers

from posts.models import Comment, Post, Group, Follow, User
from rest_framework.validators import UniqueTogetherValidator


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'text',
            'created',
            'post',
        )
        read_only_fields = ('author', 'post')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'pub_date',
            'author',
            'image',
            'group',
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
        slug_field='username'
    )

    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Пользователь уже подписан на этого автора.'
            )
        ]

    def validate(self, data):
        """Не совсем понял о чём речь про брать user из поля сериализатора
        избавился от username"""
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Подписка на самого себя запрещена!'
            )
        return data
