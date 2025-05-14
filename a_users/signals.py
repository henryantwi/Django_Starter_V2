from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            email_address = EmailAddress.objects.get_primary(instance)
            if email_address.email != instance.email:
                email_address.email = instance.email
                email_address.verified = False
                email_address.save()
        except:
            EmailAddress.objects.create(
                user=instance, email=instance.email, primary=True, verified=False
            )
    instance.profile.save()


@receiver(pre_save, sender=User)
def user_presave(sender, instance, **kwargs):
    if instance.username:
        instance.username = instance.username.lower()


@receiver(user_logged_in)
def set_onboarding_flag(sender, request, user, **kwargs):
    """Set a flag in the session to indicate the user has just logged in"""
    try:
        if not user.profile.is_onboarded:
            request.session['show_onboarding'] = True
    except:
        pass
