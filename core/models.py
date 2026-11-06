from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    """Your personal details. Only one Profile can exist."""

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, default="Full Stack Web Developer")
    tagline = models.CharField(
        max_length=200, blank=True, help_text="Short pitch shown on the home page."
    )
    bio = models.TextField()
    photo = models.ImageField(upload_to="profile/", blank=True)
    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        help_text="PDF files only.",
    )
    email = models.EmailField()
    location = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    is_available = models.BooleanField(
        default=True, help_text="Show the 'Available for work' badge."
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Always use id 1, so saving never creates a second profile
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        """Return the profile, or None if it hasn't been created yet."""
        return cls.objects.filter(pk=1).first()
