from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import ContactMessage
from portfolio.models import Experience, Project, Skill

from .forms import ProjectForm, StaffAuthenticationForm


def staff_required(view_func):
    """Only allow logged-in staff users; send everyone else to the login page."""
    return user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url="dashboard:login",
    )(view_func)


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = True


@staff_required
def home(request):
    """Dashboard overview: counts and the latest messages."""
    context = {
        "project_count": Project.objects.count(),
        "skill_count": Skill.objects.count(),
        "experience_count": Experience.objects.count(),
        "unread_count": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
    }
    return render(request, "dashboard/home.html", context)


# ---------- Projects ----------


@staff_required
def project_list(request):
    projects = Project.objects.prefetch_related("technologies")
    return render(request, "dashboard/project_list.html", {"projects": projects})


@staff_required
def project_create(request):
    form = ProjectForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        project = form.save()
        messages.success(request, f'Project "{project.title}" was created.')
        return redirect("dashboard:project_list")
    return render(
        request,
        "dashboard/project_form.html",
        {"form": form, "page_title": "Add project"},
    )


@staff_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f'Project "{project.title}" was updated.')
        return redirect("dashboard:project_list")
    context = {"form": form, "page_title": f"Edit: {project.title}", "project": project}
    return render(request, "dashboard/project_form.html", context)


@staff_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        title = project.title
        project.delete()
        messages.success(request, f'Project "{title}" was deleted.')
        return redirect("dashboard:project_list")
    context = {
        "object": project,
        "object_type": "project",
        "cancel_url": "dashboard:project_list",
    }
    return render(request, "dashboard/confirm_delete.html", context)
