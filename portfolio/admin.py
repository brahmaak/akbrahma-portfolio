from django.contrib import admin

from .models import Experience, Project, ProjectImage, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order")
    list_filter = ("category",)
    list_editable = ("proficiency", "order")
    search_fields = ("name",)


class ProjectImageInline(admin.TabularInline):
    """Lets you add screenshots on the same page as the project."""

    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_featured", "order", "created_at")
    list_filter = ("is_featured", "technologies")
    list_editable = ("is_featured", "order")
    search_fields = ("title", "summary", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "organization", "entry_type", "start_date", "end_date")
    list_filter = ("entry_type",)
