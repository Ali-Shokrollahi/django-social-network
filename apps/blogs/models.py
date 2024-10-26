from django.db import models

from apps.users.models import Profile
from apps.utils.models.timestamp import TimeStampModel


class Post(TimeStampModel):
    slug = models.SlugField(max_length=64)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=512)

    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name="posts")

    class Meta:
        unique_together = ["owner", "slug"]

    def __str__(self):
        return self.slug
