from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileForm(forms.ModelForm):
    display_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Enter your display name'
        })
    )
    
    info = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2.5 text-gray-700 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary',
            'placeholder': 'Tell us about yourself',
            'rows': 4
        })
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*'
        })
    )

    clear_image = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'display_name', 'info']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.cleaned_data.get('clear_image'):
            profile.image = None
        if commit:
            profile.save()
        return profile


class EmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email
