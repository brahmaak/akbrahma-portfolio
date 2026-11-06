from django.shortcuts import render

from portfolio.models import Experience, Project, Skill


def home(request):
    """Show the home page with featured projects and the tech stack."""
    featured_projects = Project.objects.filter(is_featured=True).prefetch_related(
        "technologies"
    )[:3]
    context = {
        "featured_projects": featured_projects,
        "skills": Skill.objects.all(),
    }
    return render(request, "core/home.html", context)


def about(request):
    """Show the About page with the experience timeline."""
    experiences = Experience.objects.all()
    return render(request, "core/about.html", {"experiences": experiences})
