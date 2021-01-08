from django.contrib.auth.models import AbstractUser
from django.db import models
from uuid import uuid4


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False, blank=True
    )
    liked_posts = models.ManyToManyField("Post", related_name="liked_by", blank=True)

    def __str__(self):
        return f"{self.username}"

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()

    def get_posts(self):
        return Post.objects.filter(author=self).order_by("-timestamp")

    def get_join_date(self):
        return self.date_joined.strftime("%b %Y")


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.PositiveIntegerField(default=0)

    def is_valid_post(self, n):
        return bool(self.content) and bool(self.number_of_likes == n)

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.id,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
            "number_of_likes": self.number_of_likes,
            "liked_by": self.liked_by,
        }
