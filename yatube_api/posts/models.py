from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200,
                             blank=False,
                             null=False)

    slug = models.SlugField(unique=True,
                            blank=False,
                            null=False)

    description = models.TextField(blank=True,
                                   null=True)

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')

    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts')

    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text

    """
    class Meta:
        ordering = ["-pub_date"]"""


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.TextField()

    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    """
    class Meta:
        ordering = ["-created"]"""


class Follow(models.Model):
    # подписчик
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )

    # автор, на которого подписан подписчик
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    constraints = [
        models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique_user_following'
        )
    ]
