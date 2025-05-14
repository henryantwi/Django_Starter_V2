from django.conf import settings

def update_default_site(sender, **kwargs):
    """
    Update the default site domain and name.
    This function is connected to the post_migrate signal in apps.py.
    """
    # Only run if the sites app has been migrated
    # Import here to avoid circular imports
    from django.contrib.sites.models import Site
    
    try:
        site = Site.objects.get(id=settings.SITE_ID)
        if hasattr(settings, 'SITE_DOMAIN') and hasattr(settings, 'SITE_NAME'):
            if site.domain != settings.SITE_DOMAIN or site.name != settings.SITE_NAME:
                site.domain = settings.SITE_DOMAIN
                site.name = settings.SITE_NAME
                site.save()
                print(f"Site updated: {site.domain} ({site.name})")
    except Site.DoesNotExist:
        # If the site doesn't exist, create it
        if hasattr(settings, 'SITE_DOMAIN') and hasattr(settings, 'SITE_NAME'):
            Site.objects.create(
                id=settings.SITE_ID,
                domain=settings.SITE_DOMAIN,
                name=settings.SITE_NAME
            )
            print(f"Site created: {settings.SITE_DOMAIN} ({settings.SITE_NAME})")
    except Exception as e:
        # Handle any other issues
        print(f"Error updating site: {str(e)}")
        