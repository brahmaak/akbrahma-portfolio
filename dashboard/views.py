from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from contact.models import ContactMessage
from core.models import Profile
from portfolio.models import Experience, Project, Skill

from .forms import (
    ExperienceForm,
    ProfileForm,
    ProjectForm,
    SkillForm,
    StaffAuthenticationForm,
)


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


# ---------- Messages ----------


@staff_required
def message_list(request):
    show = request.GET.get("filter", "all")
    all_messages = ContactMessage.objects.all()
    if show == "unread":
        all_messages = all_messages.filter(is_read=False)

    page_obj = Paginator(all_messages, 20).get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "show": show,
        "total_count": ContactMessage.objects.count(),
    }
    return render(request, "dashboard/message_list.html", context)


@staff_required
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:  # opening a message marks it as read
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "dashboard/message_detail.html", {"msg": msg})


@staff_required
@require_POST
def message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save(update_fields=["is_read"])
    messages.success(request, "Marked as read." if msg.is_read else "Marked as unread.")
    return redirect("dashboard:message_list")


@staff_required
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    return _delete_view(
        request, msg, list_url="dashboard:message_list", object_type="message"
    )


# ---------- Profile ----------


@staff_required
def profile_edit(request):
    profile = (
        Profile.load() or Profile()
    )  # edit the existing profile, or start a new one
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile was updated.")
        return redirect("dashboard:profile")
    context = {"form": form, "page_title": "Edit profile", "back_url": "dashboard:home"}
    return render(request, "dashboard/object_form.html", context)
