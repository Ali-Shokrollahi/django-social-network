from django.db import models
from django.conf import settings
from apps.utils.models.timestamp import UpdatedAtModel, CreatedAtModel


class Profile(UpdatedAtModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    post_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


class Follow(CreatedAtModel):
    follower = models.ForeignKey(Profile, related_name='followed_by', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='follows', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'following')
