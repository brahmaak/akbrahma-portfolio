from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form built from the ContactMessage model, with a honeypot."""

    # Honeypot: not part of the model, hidden from humans with CSS
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your name", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "you@example.com", "autocomplete": "email"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "What's this about?"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "rows": 6, "placeholder": "Tell me about your project..."}
            ),
        }

    def clean_message(self):
        """Require a meaningful message (at least 10 characters)."""
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least 10 characters.")
        return message

    def clean_website(self):
        """Reject the form if the hidden honeypot field was filled in."""
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""