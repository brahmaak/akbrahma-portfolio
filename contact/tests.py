from django.test import Client, TestCase
from django.urls import reverse

from contact.models import ContactMessage

VALID_DATA = {
    "name": "Visitor",
    "email": "visitor@example.com",
    "subject": "Project enquiry",
    "message": "I would like a website for my business.",
}


class ContactFormTests(TestCase):
    def setUp(self):
        self.url = reverse("contact:contact")

    def test_valid_message_is_saved_and_redirects(self):
        response = self.client.post(self.url, VALID_DATA, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, "Thanks for your message")

    def test_invalid_email_is_rejected(self):
        response = self.client.post(self.url, {**VALID_DATA, "email": "not-an-email"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_short_message_is_rejected(self):
        response = self.client.post(self.url, {**VALID_DATA, "message": "hi"})
        self.assertContains(response, "at least 10 characters")
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        self.client.post(self.url, {**VALID_DATA, "website": "http://spam.example"})
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_csrf_token_is_required(self):
        strict_client = Client(enforce_csrf_checks=True)
        response = strict_client.post(self.url, VALID_DATA)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(ContactMessage.objects.count(), 0)
