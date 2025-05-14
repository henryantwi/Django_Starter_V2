from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import valid_email_or_none
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.account.models import EmailAddress

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.
        """
        # Get the email from social account
        email = sociallogin.account.extra_data.get('email')
        if email:
            # Check if user exists with this email
            try:
                user = EmailAddress.objects.get(email=email).user
                sociallogin.connect(request, user)
            except EmailAddress.DoesNotExist:
                pass
        
        return super().pre_social_login(request, sociallogin)

    def populate_user(self, request, sociallogin, data):
        """
        Hook that can be used to further populate the user instance.
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Get extra data from Google
        extra_data = sociallogin.account.extra_data
        
        # Set email
        email = valid_email_or_none(data.get("email"))
        if email:
            user_email(user, email)
            user.email = email  # Also set user's email directly
        
        # Set username from email
        username = email.split('@')[0] if email else None
        user_username(user, username or '')
        
        # Get display name from Google data
        display_name = extra_data.get('name')
        if display_name:
            user.socialaccount_display_name = display_name
            
        # Get profile picture URL from Google data
        picture_url = extra_data.get('picture')
        if picture_url:
            user.socialaccount_picture_url = picture_url
            
        return user

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """
        user = super().save_user(request, sociallogin, form)
        
        # Verify email automatically for Google accounts
        email_address = user.emailaddress_set.get(email=user.email)
        email_address.verified = True
        email_address.save()
        
        # Set the profile display name and image after user is created
        if hasattr(user, 'profile'):
            if hasattr(user, 'socialaccount_display_name'):
                user.profile.display_name = user.socialaccount_display_name
            
            if hasattr(user, 'socialaccount_picture_url'):
                from urllib.request import urlretrieve
                from django.core.files import File
                import os
                
                # Download the image from Google
                try:
                    temp_file, _ = urlretrieve(user.socialaccount_picture_url)
                    # Save it to the profile
                    with open(temp_file, 'rb') as f:
                        user.profile.image.save(
                            f'google_avatar_{user.id}.jpg',
                            File(f),
                            save=True
                        )
                    # Clean up the temp file
                    os.unlink(temp_file)
                except Exception as e:
                    # Handle any errors silently - the user can always upload an avatar later
                    pass
            
            user.profile.save()
        
        return user

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        return '/'  # Redirect to home instead of onboarding
