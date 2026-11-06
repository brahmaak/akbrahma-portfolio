from contact.models import ContactMessage


def unread_messages(request):
    """Add the unread message count to every dashboard page (for the sidebar badge)."""
    match = request.resolver_match
    if match and match.app_name == "dashboard" and request.user.is_staff:
        return {"unread_count": ContactMessage.objects.filter(is_read=False).count()}
    return {}
