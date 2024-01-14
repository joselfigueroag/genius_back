from factory import sequence
from factory.django import DjangoModelFactory

from .models import User


class UserFactory(DjangoModelFactory):
  class Meta:
    model = User

  email = sequence(lambda n: "prueba%@gmail.com" % n)
  password = "12345678"
