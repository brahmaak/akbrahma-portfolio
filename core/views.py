from django.shortcuts import render


def home(request):
    """Show the home page."""
    return render(request, "core/home.html")


def about(request):
    """Show the About page."""
    return render(request, "core/about.html")
