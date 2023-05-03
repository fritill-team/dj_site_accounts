import random

import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

UserModel = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ('phone',)

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.lazy_attribute(
        lambda obj: '{}.{}.{}'.format(obj.first_name, obj.last_name, random.randrange(1, 1000)))
    email = factory.lazy_attribute(lambda obj: '{}@email.com'.format(obj.username))
    phone = factory.Sequence(lambda n: '3215616_%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'secret')
