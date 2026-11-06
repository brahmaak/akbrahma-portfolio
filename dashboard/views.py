from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render

from contact.models import ContactMessage
from portfolio.models import Experience, Project, Skill

from .forms import StaffAuthenticationForm


def staff_required(view_func):
    """Only allow logged-in staff users; send everyone else to the login page."""
    return user_passes_test(
        lambda user: user.is_active and user.is_staff,
        login_url="dashboard:login",
    )(view_func)


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = True  # already logged in? skip the login page


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
