from django import forms


class ContactForm(forms.Form):
    """Contact form with validation and a honeypot spam trap."""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your name",
                "autocomplete": "name",
            }
        ),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "you@example.com",
                "autocomplete": "email",
            }
        ),
    )
    subject = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "What's this about?"}
        ),
    )
    message = forms.CharField(
        min_length=10,
        max_length=3000,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Tell me about your project...",
            }
        ),
    )

    # Honeypot: hidden from humans with CSS. Bots fill in every field, so if
    # this has a value, the submission is from a bot.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    def clean_website(self):
        """Reject the form if the hidden honeypot field was filled in."""
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
