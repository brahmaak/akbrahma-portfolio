from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Skill(models.Model):
    """A technology or tool you know, e.g. Django."""

    class Category(models.TextChoices):
        FRONTEND = "frontend", "Frontend"
        BACKEND = "backend", "Backend"
        DATABASE = "database", "Database"
        TOOLS = "tools", "Tools"

    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    proficiency = models.PositiveSmallIntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Your skill level from 0 to 100.",
    )
    icon_class = models.CharField(
        max_length=50, blank=True, help_text="Bootstrap icon class, e.g. bi-filetype-py"
    )
    order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers show first."
    )

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    """A portfolio project."""

    title = models.CharField(max_length=120)
    slug = models.SlugField(
        max_length=140,
        unique=True,
        blank=True,
        help_text="Used in the URL. Leave empty to create it from the title.",
    )
    summary = models.CharField(
        max_length=250, help_text="One or two sentences for project cards."
    )
    description = models.TextField(
        help_text="Full write-up for the project detail page."
    )
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True)
    technologies = models.ManyToManyField(Skill, related_name="projects", blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False, help_text="Show on the home page.")
    order = models.PositiveSmallIntegerField(
        default=0, help_text="Lower numbers show first."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Create a unique slug from the title if none was given
        if not self.slug:
            base_slug = slugify(self.title) or "project"
            slug = base_slug
            number = 2
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{number}"
                number += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:project_detail", args=[self.slug])


class ProjectImage(models.Model):
    """An extra screenshot for a project."""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="projects/screenshots/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Screenshot of {self.project.title}"


class Experience(models.Model):
    """A job or education entry for the About page timeline."""

    class EntryType(models.TextChoices):
        WORK = "work", "Work"
        EDUCATION = "education", "Education"

    entry_type = models.CharField(
        max_length=20, choices=EntryType.choices, default=EntryType.WORK
    )
    role = models.CharField(
        max_length=100, help_text="Job title, or degree/course name."
    )
    organization = models.CharField(
        max_length=100, help_text="Company, or college/institute."
    )
    start_date = models.DateField()
    end_date = models.DateField(
        null=True, blank=True, help_text="Leave empty if this is ongoing."
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name_plural = "experience"

    def __str__(self):
        return f"{self.role} at {self.organization}"

    @property
    def is_current(self):
        return self.end_date is None

    def clean(self):
        # Extra validation: the end date can't be before the start date
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(
                {"end_date": "End date can't be before the start date."}
            )
