import factory
from django.contrib.auth import get_user_model

from apps.users.models import Profile, Follow

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    is_active = False
    is_verified = False
    is_admin = False
    profile = factory.RelatedFactory("tests.factories.ProfileFactory", factory_related_name='user')

    @factory.lazy_attribute
    def password(self):
        return "Test@1pass"

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.set_password(instance.password)
            instance.save()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    bio = factory.Faker("text", max_nb_chars=255)
    post_count = 0
    follower_count = 0
    following_count = 0


class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow

    follower = factory.SubFactory(ProfileFactory)
    following = factory.SubFactory(ProfileFactory)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        if create:
            instance.follower.following_count += 1
            instance.following.follower_count += 1
            instance.follower.save()
            instance.following.save()
