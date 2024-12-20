from django.test import override_settings, TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from .models import User


class CSVUploadTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @override_settings(RATELIMIT_VIEW='100/m')
    def test_valid_csv_upload(self):
        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Doe,jane@example.com,25"
        csv_file = SimpleUploadedFile(
            "test.csv", csv_content.encode(), content_type="text/csv")

        response = self.client.post('/api/upload_data/', {'file': csv_file})
        print("Response Content:", response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 2)

    @override_settings(RATELIMIT_VIEW='100/m')
    def test_invalid_csv_upload(self):
        csv_content = "name,email,age\n  ,invalid_email,150"
        csv_file = SimpleUploadedFile(
            "test.csv", csv_content.encode(), content_type="text/csv")

        response = self.client.post('/api/upload_data/', {'file': csv_file})
        print("Response Content:", response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)
        self.assertIn("errors", response.data)

    @override_settings(RATELIMIT_VIEW='100/m')
    def test_duplicate_email_csv_upload(self):
        User.objects.create(name="John Doe", email="john@example.com", age=30)

        csv_content = "name,email,age\nJohn Doe,john@example.com,30\nJane Doe,john@example.com,25"
        csv_file = SimpleUploadedFile(
            "test.csv", csv_content.encode(), content_type="text/csv")

        response = self.client.post('/api/upload_data/', {'file': csv_file})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
        errors = response.data.get("errors", [])
        self.assertIn("errors", response.data)
        for error in errors:
            self.assertIn("user with this email already exists.",
                          str(error.get("errorss", "")))
