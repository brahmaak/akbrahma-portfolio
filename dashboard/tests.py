from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from contact.models import ContactMessage
from portfolio.models import Project

User = get_user_model()
PASSWORD = "Strong-test-pass-123"


class DashboardAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user("staff", password=PASSWORD, is_staff=True)
        cls.visitor = User.objects.create_user("visitor", password=PASSWORD)

    def test_dashboard_pages_require_login(self):
        names = [
            "home",
            "project_list",
            "project_create",
            "skill_list",
            "skill_create",
            "experience_list",
            "experience_create",
            "message_list",
            "profile",
        ]
        for name in names:
            with self.subTest(page=name):
                url = reverse(f"dashboard:{name}")
                response = self.client.get(url)
                self.assertRedirects(
                    response, f"{reverse('dashboard:login')}?next={url}"
                )

    def test_non_staff_user_cannot_log_in(self):
        response = self.client.post(
            reverse("dashboard:login"), {"username": "visitor", "password": PASSWORD}
        )
        self.assertContains(response, "access to the dashboard")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_staff_user_can_log_in(self):
        response = self.client.post(
            reverse("dashboard:login"), {"username": "staff", "password": PASSWORD}
        )
        self.assertRedirects(response, reverse("dashboard:home"))

    def test_login_is_locked_after_five_failures(self):
        url = reverse("dashboard:login")
        for _ in range(4):
            self.client.post(url, {"username": "staff", "password": "wrong"})
        response = self.client.post(url, {"username": "staff", "password": "wrong"})
        self.assertContains(response, "Too many login attempts", status_code=429)


class DashboardCrudTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user("staff", password=PASSWORD, is_staff=True)

    def setUp(self):
        # force_login skips the password check, so django-axes isn't involved
        self.client.force_login(self.staff)

    def test_create_project(self):
        response = self.client.post(
            reverse("dashboard:project_create"),
            {
                "title": "New App",
                "slug": "",
                "summary": "S",
                "description": "D",
                "order": 0,
            },
        )
        self.assertRedirects(response, reverse("dashboard:project_list"))
        self.assertTrue(Project.objects.filter(slug="new-app").exists())

    def test_delete_needs_confirmation_by_post(self):
        project = Project.objects.create(title="Old App", summary="S", description="D")
        url = reverse("dashboard:project_delete", args=[project.pk])

        self.client.get(url)  # GET only shows the confirmation page
        self.assertTrue(Project.objects.filter(pk=project.pk).exists())

        self.client.post(url)  # POST actually deletes
        self.assertFalse(Project.objects.filter(pk=project.pk).exists())

    def test_opening_a_message_marks_it_read(self):
        msg = ContactMessage.objects.create(
            name="V", email="v@example.com", subject="Hi", message="Hello there!"
        )
        self.client.get(reverse("dashboard:message_detail", args=[msg.pk]))
        msg.refresh_from_db()
        self.assertTrue(msg.is_read)

    def test_toggle_read_rejects_get_requests(self):
        msg = ContactMessage.objects.create(
            name="V", email="v@example.com", subject="Hi", message="Hello there!"
        )
        response = self.client.get(
            reverse("dashboard:message_toggle_read", args=[msg.pk])
        )
        self.assertEqual(response.status_code, 405)

    def test_messages_are_shown_safely(self):
        msg = ContactMessage.objects.create(
            name="V",
            email="v@example.com",
            subject="Hi",
            message="<script>alert('xss')</script>",
        )
        response = self.client.get(reverse("dashboard:message_detail", args=[msg.pk]))
        self.assertNotContains(response, "<script>alert")
        self.assertContains(response, "&lt;script&gt;")
