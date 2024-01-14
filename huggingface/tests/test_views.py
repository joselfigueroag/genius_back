from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient

from ...authentication.tests.factories import UserFactory


class QueryEmotionModelView(TestCase):
  @classmethod
  def setUpTestData(cls):
    user = UserFactory()

    cls.client_drf = APIClient()

    csv_file_path = "huggingface\tests\DataRedesSociales.csv"

    with open(csv_file_path, "rb") as file:
      csv_content = file.read()
    
    uploaded_file = SimpleUploadedFile("test_data.csv", csv_content, content_type="text/csv")

  def test_success_file_processed(self):
    res = self.client_drf.post("/authentication/api/user_register/", self.data)
    self.assertEqual(res.status_code, 201)
