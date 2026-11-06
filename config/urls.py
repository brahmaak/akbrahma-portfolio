from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Admin panel branding
admin.site.site_header = "A K Brahma · Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your portfolio"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("portfolio.urls")),
    path("", include("contact.urls")),
]

# Serve uploaded files (photos, screenshots) during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
