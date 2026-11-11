from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileUpdateForm, RegistrationForm, UserUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect('notice_list')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Profile is created automatically by the post_save signal on User.
            login(request, user)
            messages.success(request, 'Your account has been created. Welcome to Campus Connect!')
            return redirect('notice_list')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    # Ensure profile exists for users created before signals/migrations were in place.
    profile_obj = getattr(request.user, 'profile', None)
    if profile_obj is None:
        from .models import Profile
        profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile_obj})


@login_required
def profile_edit(request):
    profile_obj = getattr(request.user, 'profile', None)
    if profile_obj is None:
        from .models import Profile
        profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)

    return render(request, 'accounts/profile_edit.html', {'u_form': u_form, 'p_form': p_form})
