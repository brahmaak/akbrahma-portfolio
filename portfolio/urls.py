from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("skills/", views.skills, name="skills"),
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
]
