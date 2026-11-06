from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import UploadedFile

from portfolio.models import Experience, Project, Skill

MAX_IMAGE_SIZE_MB = 2


class BootstrapFormMixin:
    """Adds the right Bootstrap CSS class to every field automatically."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.CheckboxSelectMultiple)):
                widget.attrs["class"] = "form-check-input"
            elif isinstance(widget, forms.Select):
                widget.attrs["class"] = "form-select"
            else:
                widget.attrs["class"] = "form-control"


class StaffAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    """Login form that only lets staff users in."""

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError(
                "This account doesn't have access to the dashboard.", code="no_access"
            )


def validate_image_size(image):
    """Reject newly uploaded images larger than MAX_IMAGE_SIZE_MB."""
    if isinstance(image, UploadedFile) and image.size > MAX_IMAGE_SIZE_MB * 1024 * 1024:
        raise forms.ValidationError(
            f"Image must be smaller than {MAX_IMAGE_SIZE_MB} MB."
        )
    return image


class ProjectForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "summary",
            "description",
            "thumbnail",
            "technologies",
            "github_url",
            "live_url",
            "is_featured",
            "order",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 10}),
            "technologies": forms.CheckboxSelectMultiple,
        }

    def clean_thumbnail(self):
        return validate_image_size(self.cleaned_data.get("thumbnail"))


class SkillForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["name", "category", "proficiency", "icon_class", "order"]
        widgets = {
            "proficiency": forms.NumberInput(attrs={"min": 0, "max": 100}),
        }


class ExperienceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "entry_type",
            "role",
            "organization",
            "start_date",
            "end_date",
            "description",
        ]
        widgets = {
            # type="date" shows the browser's date picker; the format pre-fills it when editing
            "start_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "end_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
