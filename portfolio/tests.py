from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from portfolio.models import Experience, Project, Skill


class ProjectModelTests(TestCase):
    def test_slug_is_created_from_title(self):
        project = Project.objects.create(
            title="My Great App", summary="S", description="D"
        )
        self.assertEqual(project.slug, "my-great-app")

    def test_duplicate_titles_get_unique_slugs(self):
        first = Project.objects.create(title="Same Name", summary="S", description="D")
        second = Project.objects.create(title="Same Name", summary="S", description="D")
        self.assertEqual(first.slug, "same-name")
        self.assertEqual(second.slug, "same-name-2")

    def test_get_absolute_url(self):
        project = Project.objects.create(title="Blog", summary="S", description="D")
        self.assertEqual(project.get_absolute_url(), "/projects/blog/")


class ExperienceModelTests(TestCase):
    def test_end_date_before_start_date_is_invalid(self):
        entry = Experience(
            role="Dev",
            organization="Acme",
            start_date=date(2024, 6, 1),
            end_date=date(2023, 1, 1),
        )
        with self.assertRaises(ValidationError):
            entry.full_clean()

    def test_is_current_when_no_end_date(self):
        entry = Experience(role="Dev", organization="Acme", start_date=date(2024, 1, 1))
        self.assertTrue(entry.is_current)


class PortfolioPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.django = Skill.objects.create(
            name="Django", category="backend", proficiency=80
        )
        Skill.objects.create(name="HTML5", category="frontend", proficiency=90)
        cls.project = Project.objects.create(
            title="Task Manager", summary="Track tasks.", description="Full write-up."
        )
        cls.project.technologies.add(cls.django)

    def test_skills_page_groups_skills_by_category(self):
        response = self.client.get(reverse("portfolio:skills"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Frontend")
        self.assertContains(response, "Backend")
        self.assertNotContains(response, "Tools")  # empty categories are hidden

    def test_projects_page_lists_projects_and_used_technologies(self):
        response = self.client.get(reverse("portfolio:projects"))
        self.assertContains(response, "Task Manager")
        self.assertContains(response, 'data-filter="Django"')
        self.assertNotContains(
            response, 'data-filter="HTML5"'
        )  # not used by any project

    def test_project_detail_page(self):
        response = self.client.get(self.project.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full write-up.")

    def test_unknown_project_returns_404(self):
        response = self.client.get("/projects/does-not-exist/")
        self.assertEqual(response.status_code, 404)
