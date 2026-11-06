from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.DashboardLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # Projects
    path("projects/", views.project_list, name="project_list"),
    path("projects/add/", views.project_create, name="project_create"),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),
    # Skills
    path("skills/", views.skill_list, name="skill_list"),
    path("skills/add/", views.skill_create, name="skill_create"),
    path("skills/<int:pk>/edit/", views.skill_update, name="skill_update"),
    path("skills/<int:pk>/delete/", views.skill_delete, name="skill_delete"),
    # Experience
    path("experience/", views.experience_list, name="experience_list"),
    path("experience/add/", views.experience_create, name="experience_create"),
    path(
        "experience/<int:pk>/edit/", views.experience_update, name="experience_update"
    ),
    path(
        "experience/<int:pk>/delete/", views.experience_delete, name="experience_delete"
    ),
]
