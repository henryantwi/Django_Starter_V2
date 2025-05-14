from django.shortcuts import render, redirect


def home_view(request):
    # Check if user is authenticated and needs onboarding
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if not profile.is_onboarded and 'show_onboarding' in request.session:
                # Redirect to onboarding page
                return redirect('profile-onboarding')
        except:
            pass
            
    return render(request, "home.html")
