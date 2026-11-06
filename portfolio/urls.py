from django.urls import path

from . import views

app_name = "portfolio"

urlpatterns = [
    path("skills/", views.skills, name="skills"),
]
