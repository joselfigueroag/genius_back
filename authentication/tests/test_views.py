from django.test import TestCase

from rest_framework.test import APIClient

from ..models import User
from .factories import UserFactory


class UserViewSetTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    UserFactory()

    cls.client_drf = APIClient()

    cls.data = {
      "email": "test@prueba.com",
      "password": "12345678",
    }

  def test_success_register_user(self):
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    self.assertEqual(res.status_code, 201)

  def test_email_already_registered(self):
    self.data["email"] = User.objects.last().email
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("msg"), "Correo electronico ya registrado")

  def test_empty_data(self):
    self.data["email"] = ""
    self.data["password"] = ""
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("msg"), "Los campos no pueden estar vacios")

  def test_invalid_email(self):
    self.data["email"] = "prueba"
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("email")[0].__str__(), "Enter a valid email address.")


class LoginViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.client_drf = APIClient()

    user = UserFactory()

    cls.data = {
      "email": user.email,
      "password": "12345678"
    }

  def test_success_login(self):
    res = self.client_drf.post("/authentication/api/login/", self.data)
    self.assertEqual(res.status_code, 200)

  def test_email_is_not_registered(self):
    self.data["email"] = "ya@existe.com"
    res = self.client_drf.post("/authentication/api/login/", self.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(res.data.get("msg"), "Correo electronico no registrado")

  def test_empty_data(self):
    self.data["email"] = ""
    self.data["password"] = ""
    res = self.client_drf.post("/authentication/api/login/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("msg"), "Debe introducir correo y contraseña")


class LogoutViewTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = UserFactory()

    cls.client_drf = APIClient()

    cls.data = {
      "email": cls.user.email,
      "password": "12345678"
    }

  def test_fail_logout(self):
    res = self.client_drf.get("/authentication/api/logout/")
    self.assertEqual(res.status_code, 401)
    self.assertEqual(res.data.get("detail").__str__(), "Authentication credentials were not provided.")

  def test_success_logout(self):
    self.client_drf.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
    res = self.client_drf.get("/authentication/api/logout/")
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.data.get("msg").__str__(), "Cierre de sesión exitoso")
