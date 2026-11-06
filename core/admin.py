from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "is_available", "updated_at")

    def has_add_permission(self, request):
        # Hide the "Add" button once a profile exists (there can only be one)
        return not Profile.objects.exists()
