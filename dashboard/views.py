from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import ContactMessage
from portfolio.models import Experience, Project, Skill

from .forms import ExperienceForm, ProjectForm, SkillForm, StaffAuthenticationForm


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


# ---------- Reusable helpers ----------


def _form_view(
    request, form_class, *, list_url, page_title, object_type, instance=None
):
    """Show and process an Add/Edit form for any model."""
    form = form_class(request.POST or None, request.FILES or None, instance=instance)
    if request.method == "POST" and form.is_valid():
        obj = form.save()
        action = "updated" if instance else "created"
        messages.success(request, f'{object_type.capitalize()} "{obj}" was {action}.')
        return redirect(list_url)
    context = {"form": form, "page_title": page_title, "back_url": list_url}
    return render(request, "dashboard/object_form.html", context)


def _delete_view(request, obj, *, list_url, object_type):
    """Ask for confirmation (GET), then delete (POST) any object."""
    if request.method == "POST":
        label = str(obj)
        obj.delete()
        messages.success(request, f'{object_type.capitalize()} "{label}" was deleted.')
        return redirect(list_url)
    context = {"object": obj, "object_type": object_type, "cancel_url": list_url}
    return render(request, "dashboard/confirm_delete.html", context)


# ---------- Overview ----------


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
    return _delete_view(
        request, project, list_url="dashboard:project_list", object_type="project"
    )


# ---------- Skills ----------


@staff_required
def skill_list(request):
    return render(request, "dashboard/skill_list.html", {"skills": Skill.objects.all()})


@staff_required
def skill_create(request):
    return _form_view(
        request,
        SkillForm,
        list_url="dashboard:skill_list",
        page_title="Add skill",
        object_type="skill",
    )


@staff_required
def skill_update(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return _form_view(
        request,
        SkillForm,
        instance=skill,
        list_url="dashboard:skill_list",
        page_title=f"Edit: {skill.name}",
        object_type="skill",
    )


@staff_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    return _delete_view(
        request, skill, list_url="dashboard:skill_list", object_type="skill"
    )


# ---------- Experience ----------


@staff_required
def experience_list(request):
    return render(
        request, "dashboard/experience_list.html", {"entries": Experience.objects.all()}
    )


@staff_required
def experience_create(request):
    return _form_view(
        request,
        ExperienceForm,
        list_url="dashboard:experience_list",
        page_title="Add experience",
        object_type="entry",
    )


@staff_required
def experience_update(request, pk):
    entry = get_object_or_404(Experience, pk=pk)
    return _form_view(
        request,
        ExperienceForm,
        instance=entry,
        list_url="dashboard:experience_list",
        page_title=f"Edit: {entry.role}",
        object_type="entry",
    )


@staff_required
def experience_delete(request, pk):
    entry = get_object_or_404(Experience, pk=pk)
    return _delete_view(
        request, entry, list_url="dashboard:experience_list", object_type="entry"
    )
