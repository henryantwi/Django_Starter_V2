from allauth.account.utils import send_email_confirmation
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from allauth.account.views import EmailVerificationSentView

from .forms import EmailForm, ProfileForm
from .models import Profile


# Custom view to override allauth's email verification sent page
class CustomEmailVerificationSentView(EmailVerificationSentView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["email_url"] = reverse("account_resend_email")

        # Add the email to the context if available in the session
        email = self.request.session.get("account_verification_email")
        if email:
            context["email"] = email

        # Check if a verification email was just successfully sent
        if self.request.session.get("verification_email_sent"):
            context["resent"] = True
            # Clear the flag after using it
            del self.request.session["verification_email_sent"]

        return context

    def get(self, request, *args, **kwargs):
        # Store the email in the session if available in the request
        if hasattr(request, "user") and request.user.is_authenticated:
            request.session["account_verification_email"] = request.user.email

        # Get email from allauth if available
        email = request.GET.get("email", None)
        if email:
            request.session["account_verification_email"] = email
            
        # Also get email from the post data if available
        if request.method == "POST" and "email" in request.POST:
            request.session["account_verification_email"] = request.POST.get("email")

        return super().get(request, *args, **kwargs)


# @login_required
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(Profile, user__username=username)
    else:
        if not request.user.is_authenticated:
            return redirect("account_login")
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return redirect("account_login")

    return render(request, "a_users/profile.html", {"profile": profile})


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")

    if request.path == reverse("profile-onboarding"):
        onboarding = True
    else:
        onboarding = False

    context = {
        "form": form,
        "onboarding": onboarding,
    }

    return render(request, "a_users/profile_edit.html", context)


@login_required
def onboarding_view(request):
    """Handle the onboarding process"""
    form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.is_onboarded = True
            profile.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")

    context = {
        "form": form,
        "onboarding": True,
    }
    return render(request, "a_users/profile_edit.html", context)


@login_required
def profile_settings_view(request):
    return render(request, "a_users/profile_settings.html")


@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, "partials/email_form.html", {"form": form})
    if request.method == "POST":
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                messages.warning(request, f"{email} is already in use.")
                return redirect("profile-settings")
            form.save()
            send_email_confirmation(request, request.user)
            return redirect("profile-settings")
        else:
            messages.error(request, "Invalid email.")
            return redirect("profile-settings")
    return redirect("home")


@login_required
def profile_emailverify(request):
    send_email_confirmation(request, request.user)
    return redirect("profile-settings")


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect("home")
    return render(request, "a_users/profile_delete.html")


# View to handle resending verification emails
def resend_email_verification(request):
    success = False

    # Form submission for entering email
    if request.method == "POST" and "email" in request.POST:
        email = request.POST.get("email")
        if email:
            try:
                user = User.objects.get(email=email)
                send_email_confirmation(request, user)
                messages.success(request, "A new verification email has been sent.")
                success = True
                
                # Store the email in the session for future use
                request.session["account_verification_email"] = email
            except User.DoesNotExist:
                messages.error(
                    request,
                    "No account found with this email address. Please check the email or sign up.",
                )
                return render(
                    request, 
                    "account/resend_verification.html", 
                    {"form_email": email}
                )
    # Authenticated user
    elif request.user.is_authenticated:
        send_email_confirmation(request, request.user)
        messages.success(request, "A new verification email has been sent.")
        success = True
    # Try to get email from session
    else:
        email = request.session.get("account_verification_email")
        if email:
            try:
                user = User.objects.get(email=email)
                send_email_confirmation(request, user)
                messages.success(request, "A new verification email has been sent.")
                success = True
            except User.DoesNotExist:
                # Show form to input email
                return render(
                    request, 
                    "account/resend_verification.html", 
                    {}
                )
        else:
            # No email in session, show form
            return render(
                request, 
                "account/resend_verification.html", 
                {}
            )

    # Store success status in session
    request.session["verification_email_sent"] = success
    return redirect("account_email_verification_sent")
