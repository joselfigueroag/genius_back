from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from authentication.tests.factories import UserFactory


class QueryEmotionModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = UserFactory()

    cls.client_drf = APIClient()

    csv_file_path = "huggingface/tests/DataRedesSociales.csv"

    with open(csv_file_path, "rb") as file:
      csv_content = file.read()

    uploaded_file = SimpleUploadedFile("test_data.csv", csv_content, content_type="text/csv")

    cls.data = {
      "file": uploaded_file
    }

  def test_attempt_file_process_without_token(self):
    res = self.client_drf.post("/huggingface/api/query_emotion_model/", self.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(res.data.get("detail").__str__(), "Authentication credentials were not provided.")
  
  def test_success_processed_file(self):
    self.client_drf.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
    res = self.client_drf.post("/huggingface/api/query_emotion_model/", self.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.data["motive"], "emotions")

  def test_attempt_file_process_without_file(self):
    self.client_drf.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
    self.data["file"] = ""
    res = self.client_drf.post("/huggingface/api/query_emotion_model/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("msg"), "Debe cargar un archivo CSV")
  

class QuerySentimentModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    cls.user = UserFactory()

    cls.client_drf = APIClient()

    csv_file_path = "huggingface/tests/DataRedesSociales.csv"

    with open(csv_file_path, "rb") as file:
      csv_content = file.read()

    uploaded_file = SimpleUploadedFile("test_data.csv", csv_content, content_type="text/csv")

    cls.data = {
      "file": uploaded_file
    }

  def test_attempt_file_process_without_token(self):
    res = self.client_drf.post("/huggingface/api/query_sentiment_model/", self.data)
    self.assertEqual(res.status_code, 401)
    self.assertEqual(res.data.get("detail").__str__(), "Authentication credentials were not provided.")
  
  def test_success_processed_file(self):
    self.client_drf.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
    res = self.client_drf.post("/huggingface/api/query_sentiment_model/", self.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(res.data["motive"], "sentiments")

  def test_attempt_file_process_without_file(self):
    self.client_drf.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
    self.data["file"] = ""
    res = self.client_drf.post("/huggingface/api/query_sentiment_model/", self.data)
    self.assertEqual(res.status_code, 400)
    self.assertEqual(res.data.get("msg"), "Debe cargar un archivo CSV")
