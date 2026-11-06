from django.shortcuts import get_object_or_404, render

from .models import Project, Skill

# Icon shown next to each skill category on the Skills page
CATEGORY_ICONS = {
    "frontend": "bi-window-sidebar",
    "backend": "bi-server",
    "database": "bi-database",
    "tools": "bi-tools",
}


def skills(request):
    """Show skills grouped by category."""
    all_skills = list(Skill.objects.all())  # one database query

    skill_groups = []
    for value, label in Skill.Category.choices:  # keeps Frontend → Tools order
        group_skills = [skill for skill in all_skills if skill.category == value]
        if group_skills:  # skip empty categories
            skill_groups.append(
                {
                    "category": label,
                    "icon": CATEGORY_ICONS[value],
                    "skills": group_skills,
                }
            )

    return render(request, "portfolio/skills.html", {"skill_groups": skill_groups})


def projects(request):
    """Show all projects with technology filter buttons."""
    projects = Project.objects.prefetch_related("technologies")
    # Only show filter buttons for technologies that are used in a project
    technologies = (
        Skill.objects.filter(projects__isnull=False).distinct().order_by("name")
    )
    context = {"projects": projects, "technologies": technologies}
    return render(request, "portfolio/projects.html", context)


def project_detail(request, slug):
    """Show one project, found by its slug."""
    project = get_object_or_404(
        Project.objects.prefetch_related("technologies", "images"), slug=slug
    )
    other_projects = Project.objects.exclude(pk=project.pk).prefetch_related(
        "technologies"
    )[:3]
    context = {"project": project, "other_projects": other_projects}
    return render(request, "portfolio/project_detail.html", context)
