from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StaffAuthenticationForm(AuthenticationForm):
    """Login form that only lets staff users in, styled with Bootstrap."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # rejects inactive accounts
        if not user.is_staff:
            raise forms.ValidationError(
                "This account doesn't have access to the dashboard.", code="no_access"
            )
