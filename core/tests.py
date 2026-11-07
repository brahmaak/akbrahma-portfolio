from datetime import date

from django.test import TestCase
from django.urls import reverse

from core.models import Profile
from portfolio.models import Experience, Project


class ProfileModelTests(TestCase):
    def test_only_one_profile_can_exist(self):
        Profile.objects.create(name="First", bio="Bio", email="first@example.com")
        Profile.objects.create(name="Second", bio="Bio", email="second@example.com")
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(Profile.load().name, "Second")

    def test_load_returns_none_when_no_profile(self):
        self.assertIsNone(Profile.load())


class EmptySiteTests(TestCase):
    """The site must still work before any content is added."""

    def test_home_page_works_without_a_profile(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A K Brahma")  # the |default value


class CorePageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Profile.objects.create(
            name="Test Developer",
            title="Full Stack Web Developer",
            tagline="I build web apps.",
            bio="First paragraph.\n\nSecond paragraph.",
            email="dev@example.com",
        )

    def test_home_page_shows_profile(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Developer")
        self.assertContains(response, "I build web apps.")

    def test_home_page_shows_only_featured_projects(self):
        Project.objects.create(
            title="Featured App", summary="S", description="D", is_featured=True
        )
        Project.objects.create(
            title="Hidden App", summary="S", description="D", is_featured=False
        )
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Featured App")
        self.assertNotContains(response, "Hidden App")

    def test_about_page_shows_bio_and_experience(self):
        Experience.objects.create(
            role="Junior Developer",
            organization="Acme Ltd",
            start_date=date(2024, 1, 1),
        )
        response = self.client.get(reverse("core:about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<p>Second paragraph.</p>", html=True)
        self.assertContains(response, "Junior Developer")
        self.assertContains(response, "Present")  # no end date means "Present"
