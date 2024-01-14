from django.contrib.auth.hashers import make_password

from factory import sequence, SubFactory, RelatedFactory
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token

from ..models import User


class UserFactory(DjangoModelFactory):
  class Meta:
    model = User

  email = sequence(lambda n: f"prueba{n}@gmail.com")
  password = make_password("12345678")

  auth_token = RelatedFactory(
    'authentication.tests.factories.TokenFactory',
    factory_related_name='user',
  )


class TokenFactory(DjangoModelFactory):
  class Meta:
    model = Token
  
  user = SubFactory(UserFactory)
