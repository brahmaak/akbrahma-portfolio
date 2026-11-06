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
]
