from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django_resized import ResizedImageField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to="avatars/", null=True, blank=True)
    image = ResizedImageField(
        size=[600, 600],
        quality=85,
        upload_to="avatars/",
        null=True,
        blank=True,
    )
    display_name = models.CharField(max_length=50, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    is_onboarded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @property
    def name(self):
        if self.display_name:
            name = self.display_name
        else:
            name = self.user.username
        return name

    @property
    def avatar(self):
        try:
            avatar = self.image.url
        except:
            avatar = static("images/avatar.svg")
        return avatar
