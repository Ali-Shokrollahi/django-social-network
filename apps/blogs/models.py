from django.db import models

from apps.users.models import Profile
from apps.utils.models.timestamp import TimeStampModel, CreatedAtModel


class Post(TimeStampModel):
    slug = models.SlugField(max_length=64)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=512)

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="posts")

    class Meta:
        unique_together = ["owner", "slug"]

    def __str__(self):
        return self.slug


class Like(CreatedAtModel):
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ('profile', 'post')

    def __str__(self):
        return f"{self.profile.username} likes {self.post}"
