from django.urls import path
from allauth.account.views import email_verification_sent

from .views import *

urlpatterns = [
    path("", profile_view, name="profile"),
    path("edit/", profile_edit_view, name="profile-edit"),
    path("onboarding/", onboarding_view, name="profile-onboarding"),
    path("settings/", profile_settings_view, name="profile-settings"),
    path("emailchange/", profile_emailchange, name="profile-emailchange"),
    path("emailverify/", profile_emailverify, name="profile-emailverify"),
    path("delete/", profile_delete_view, name="profile-delete"),
    path(
        "resend-verification/",
        resend_email_verification,
        name="resend_email_verification",
    ),
]
