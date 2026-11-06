from django.shortcuts import render

from portfolio.models import Experience


def home(request):
    """Show the home page."""
    return render(request, "core/home.html")


def about(request):
    """Show the About page with the experience timeline."""
    experiences = Experience.objects.all()  # newest first (from Meta.ordering)
    return render(request, "core/about.html", {"experiences": experiences})
