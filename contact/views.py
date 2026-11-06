from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm


def contact(request):
    """Show the contact form and handle submissions."""
    if request.method == "POST":
        # The user submitted the form: fill it with their data and validate
        form = ContactForm(request.POST)
        if form.is_valid():
            # Phase 8: save the message to the database here
            messages.success(
                request, "Thanks for your message! I'll get back to you soon."
            )
            return redirect("contact:contact")  # POST → Redirect → GET
    else:
        # First visit: show an empty form
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
