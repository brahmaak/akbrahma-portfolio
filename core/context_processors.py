from .models import Profile


def profile(request):
    """Make the profile available in every template as {{ profile }}."""
    return {"profile": Profile.load()}
