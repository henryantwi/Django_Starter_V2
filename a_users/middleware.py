from django.shortcuts import redirect
from django.urls import resolve, reverse


class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            current_url = request.path_info
            
            # Skip middleware for these paths
            excluded_paths = [
                '/', 
                reverse('profile-onboarding'),
                '/admin', 
                '/static', 
                '/media',
                '/accounts/logout/'
            ]
            
            # Check if current URL is in excluded paths or starts with excluded path prefixes
            should_skip = any(
                current_url == path or 
                (not path.endswith('/') and current_url.startswith(path + '/')) or
                (path != '/' and current_url.startswith(path))
                for path in excluded_paths
            )
            
            # Also skip AJAX/HTMX requests
            if should_skip or \
               request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
               request.headers.get('HX-Request'):
                return self.get_response(request)
            
            # Check if user needs onboarding
            try:
                profile = request.user.profile
                if not profile.is_onboarded and 'show_onboarding' in request.session:
                    # Clear the session flag to prevent redirect loops
                    del request.session['show_onboarding']
                    request.session.modified = True
                    return redirect('profile-onboarding')
            except:
                # Profile doesn't exist or some other error
                pass
            
        return self.get_response(request)
