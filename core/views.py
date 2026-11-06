from django.shortcuts import render


def home(request):
    """Show the home page."""
    return render(request, "core/home.html")
