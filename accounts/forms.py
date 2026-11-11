from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegistrationForm(UserCreationForm):
    """Registration creates a Django User; a Profile is auto-created by signal.

    New registrations default to the Student role. Authorized publisher roles
    should be assigned by an administrator (not self-selected here).
    """

    email = forms.EmailField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('department', 'bio')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
