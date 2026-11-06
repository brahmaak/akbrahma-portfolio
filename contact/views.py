from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ContactForm


def contact(request):
    """Show the contact form and save valid submissions."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # creates a ContactMessage row in PostgreSQL
            messages.success(
                request, "Thanks for your message! I'll get back to you soon."
            )
            return redirect("contact:contact")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
