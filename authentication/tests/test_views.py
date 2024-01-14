from django.test import TestCase

from rest_framework.test import APIClient

from .models import User
from .tests.factories import UserFactory


class UserViewSetTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    UserFactory()

    cls.client_drf = APIClient()

    cls.data = {
      "email": "test@prueba.com",
      "password": "12345678",
    }

  def test_register_user(self):
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    import ipdb ; ipdb.set_trace()
    pass
