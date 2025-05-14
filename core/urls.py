from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from a_home.views import *
from a_users.views import (
    profile_view,
    CustomEmailVerificationSentView,
    resend_email_verification,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Override the default allauth email verification sent view
    path(
        "accounts/confirm-email/",
        CustomEmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
    path(
        "accounts/resend-email/", resend_email_verification, name="account_resend_email"
    ),
    # Include the rest of the allauth URLs
    path("accounts/", include("allauth.urls")),
    path("", home_view, name="home"),
    path("profile/", include("a_users.urls")),
    path("@<username>/", profile_view, name="profile"),
]

# Only used in developement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
