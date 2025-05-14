from django.apps import AppConfig

class AUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_users'

    def ready(self):
        # Import signals
        import a_users.signals
        
        # Import and register the post_migrate handler
        from django.db.models.signals import post_migrate
        from .site_utils import update_default_site
        post_migrate.connect(update_default_site, sender=self)
        